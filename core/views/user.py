from rest_framework.viewsets import ModelViewSet

from core.models import User
from core.serializers.user import userSerializer

from rest_framework.permissions import IsAuthenticated

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return User.objects.none()

        if user.role == 'admin':
            return User.objects.all()
        elif user.role == 'padrao':
            return User.objects.filter(id=user.id)
        return User.objects.none()

