from rest_framework.viewsets import ModelViewSet
from core.models import User
from core.serializers.user import userSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.all()
        elif user.role == 'padrao':
            return User.objects.filter(id=user.id)
        return User.objects.none()

