from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "email": user.email,
        "avatar": user.profile.avatar_url if hasattr(user, "profile") else "",
        "name": user.get_full_name(),
    })