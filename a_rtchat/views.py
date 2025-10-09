# path: a_rtchat/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import PrivateChat, GroupMessage
from .serializers import MessageSerializer, PrivateChatSerializer

User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_my_chats(request):
    """
    Retorna lista de PrivateChat onde request.user participa.
    """
    user = request.user
    chats = PrivateChat.objects.filter(participants=user).order_by("-created")
    serializer = PrivateChatSerializer(chats, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def chat_messages(request, chat_id):
    """
    GET: lista mensagens de um chat privado (apenas se for participante).
    POST: cria mensagem nesse chat (apenas se for participante).
    """
    user = request.user
    chat = get_object_or_404(PrivateChat, chat_id=chat_id)

    # proteção: somente participantes
    if not chat.has_participant(user):
        # Forçar 404 para não revelar existência
        raise Http404()

    if request.method == "GET":
        messages = chat.chat_messages.order_by("created")[:200]
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    # POST -> criar mensagem
    body = request.data.get("body", "")
    file = request.FILES.get("file", None)
    msg = GroupMessage.objects.create(chat=chat, author=user, body=body, file=file)

    # broadcast via channels (mantemos o comportamento anterior)
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_{chat.chat_id}",
        {
            "type": "chat_message",
            "id": msg.id,
            "author": msg.author.username,
            "message": msg.body,
            "file": msg.file.url if msg.file else None,
            "created": msg.created.isoformat(),
        },
    )

    serializer = MessageSerializer(msg)
    return Response(serializer.data, status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_or_get_private_chat(request):
    """
    Body: { "other_user_id": 123 } ou { "other_username": "fulano" }
    Retorna o chat_id existente entre request.user e other user, ou cria um novo.
    """
    user = request.user

    other_id = request.data.get("other_user_id")
    other_username = request.data.get("other_username")

    if not other_id and not other_username:
        return Response({"error": "Provide other_user_id or other_username"}, status=400)

    try:
        if other_id:
            other = User.objects.get(pk=other_id)
        else:
            other = User.objects.get(username=other_username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    # Se tentar criar conversa consigo mesmo -> erro
    if other.pk == user.pk:
        return Response({"error": "Cannot create private chat with yourself"}, status=400)

    # Procurar chat que contenha exatamente esses dois participantes.
    # Simples estratégia: filtrar chats onde participants incluem user e other, e que tenham exactly 2 participants.
    chats = PrivateChat.objects.filter(participants=user).filter(participants=other)
    for c in chats:
        if c.participants.count() == 2:
            serializer = PrivateChatSerializer(c)
            return Response(serializer.data)

    # se não existiu -> cria
    new_chat = PrivateChat.objects.create()
    new_chat.participants.add(user, other)
    new_chat.save()

    serializer = PrivateChatSerializer(new_chat)
    return Response(serializer.data, status=201)
