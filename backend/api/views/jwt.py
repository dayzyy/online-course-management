from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from api.serializers.jwt import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        request=CustomTokenObtainPairSerializer,
        responses={200: {'type': 'object', 'properties': {'access': {'type': 'string'}, 'refresh': {'type': 'string'}}}},
        description="Obtain JWT access and refresh tokens using email and password"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
