from rest_framework import serializers
from domain.models import CustomUser

class RegisterUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=CustomUser.Roles.choices,
        error_messages={
            'invalid_choice': f'Choose role from {[r[1] for r in CustomUser.Roles.choices]}'
        }
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "last_login": {"read_only": True}
        }
