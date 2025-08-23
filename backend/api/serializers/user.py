from rest_framework import serializers
from domain.models import CustomUser

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True}
        }
