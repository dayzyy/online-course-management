from rest_framework import generics
from rest_framework.permissions import AllowAny
from api.serializers.user import RegisterUserSerializer
from domain.models import CustomUser

class Register(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
