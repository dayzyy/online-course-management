from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    print("HEREEEEEEEE")
    username_field = 'email'

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        print("CREDENTIALS:", credentials)
        user = authenticate(**credentials)

        if user:
            print("USER EXISTS")
            data = {}
            refresh = self.get_token(user)

            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            return data
        else:
            raise exceptions.AuthenticationFailed('No active account found with the given credentials')
