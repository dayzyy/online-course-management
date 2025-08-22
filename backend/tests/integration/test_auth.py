from django.urls import reverse
from rest_framework.test import APIClient
from domain.models import CustomUser

def test_custom_user_can_obtain_jwt_tokens(default_user: CustomUser, default_user_password: str):
    path = reverse('token_obtain_pair')

    client = APIClient()
    response = client.post(path, {"email": default_user.email, "password": default_user_password}, format="json")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

def test_custom_user_can_refresh_token(default_user: CustomUser, default_user_password: str):
    path = reverse('token_obtain_pair')

    client = APIClient()
    response = client.post(path, {"email": default_user.email, "password": default_user_password}, format="json")

    refresh_token = response.data['refresh']

    path = reverse('token_refresh')
    response = client.post(path, {"refresh": refresh_token}, format="json")

    assert response.status_code == 200
    assert "access" in response.data
