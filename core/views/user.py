from rest_framework.viewsets import ModelViewSet

from rest_framework import generics
from core.serializers.user import UserCreateSerializer

from core.models import User
from core.serializers.user import userSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny

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

# CADASTRO users
    
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny] 

