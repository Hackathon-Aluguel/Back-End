# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import ChatGroup, GroupMessage
from .serializers import MessageSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ChatGroup, GroupMessage
from .forms import ChatmessageCreateForm
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
User = get_user_model()



from django.http import JsonResponse

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def group_messages(request, group_name):
    group = get_object_or_404(ChatGroup, group_name=group_name)

    if request.method == 'GET':
        # últimos 50, ordenados por data
        messages = group.chat_messages.order_by('created')[:50]
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        body = request.data.get('body', '')
        file = request.FILES.get('file')
        msg = GroupMessage.objects.create(
            group=group,
            author=request.user,
            body=body,
            file=file
        )

        # broadcast pelo channel_layer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{group_name}",
            {
                "type": "chat_message",
                "author": request.user.username,
                "message": msg.body,
                "message_id": msg.id,
                "file": msg.file.url if msg.file else None,
                "created": msg.created.isoformat()
            }
        )

        serializer = MessageSerializer(msg)
        return Response(serializer.data, status=201)

@login_required 
def chat_messages_api(request, chatroom_name):
        chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        messages = chat_group.chat_messages.all()[:50]
        return JsonResponse([ { 'id': m.id, 'author': m.author.username, 'body': m.body, 'created': m.created.isoformat() } for m in messages ], safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_messages_api(request, chatroom_name):
    group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    messages = group.chat_messages.all()[:50]
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_file_upload(request, chatroom_name):
    group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    file = request.FILES.get('file')
    if file:
        msg = GroupMessage.objects.create(group=group, author=request.user, file=file)
        return Response({"id": msg.id, "file": msg.file.url})
    return Response({"error": "No file"}, status=400)

def get_private_chatrooms(user):
    chatrooms = user.chat_groups.filter(is_private=True).distinct()
    for chatroom in chatrooms:
        chatroom.other_member = chatroom.members.exclude(id=user.id).first()
    return chatrooms

@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private and request.user not in chat_group.members.all():
        raise Http404()
    if chat_group.is_private:
        other_user = chat_group.members.exclude(id=request.user.id).first()

    if request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            # Envia para WebSocket
            channel_layer = get_channel_layer()
            event = {
                'type': 'chat_message',
                'message': message.body,
                'author': request.user.username,
                'message_id': message.id,
            }
            async_to_sync(channel_layer.group_send)(chatroom_name, event)

            return render(request, 'a_rtchat/partials/chat_message_p.html', {'message': message, 'user': request.user})

    chatrooms = get_private_chatrooms(request.user)
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        'chatrooms': chatrooms,
        'chat_group': chat_group,
    }
    return render(request, 'a_rtchat/chat.html', context)

@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    chatroom = next((room for room in my_chatrooms if other_user in room.members.all()), None)

    if not chatroom:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

        return redirect('chatroom', chatroom_name=chatroom.group_name)


    # return HttpResponse()
    return JsonResponse({"status": "ok"})
