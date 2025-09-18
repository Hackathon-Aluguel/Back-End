from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    profile = getattr(user, "profile", None)

    data = {
        "username": user.username,
        "name": user.name,              
        "avatar": user.avatar,           
        "bio": profile.bio if profile else "",
    }
    return JsonResponse(data)

