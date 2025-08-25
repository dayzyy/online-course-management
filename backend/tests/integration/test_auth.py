import pytest
from django.urls import reverse
from domain.models import CustomUser
from rest_framework.test import APIClient

def get_tokens(api_client: APIClient, email, password):
    path = reverse('token_obtain_pair')
    return api_client.post(path, {"email": email, "password": password}, format="json")

def test_custom_user_can_obtain_jwt_tokens(api_client: APIClient, default_user: CustomUser, default_user_password: str):
    response = get_tokens(api_client, default_user.email, default_user_password)

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

def test_custom_user_can_refresh_token(api_client: APIClient, default_user: CustomUser, default_user_password: str):
    response = get_tokens(api_client, default_user.email, default_user_password)
    refresh_token = response.data['refresh']

    path = reverse('token_refresh')
    response = api_client.post(path, {"refresh": refresh_token}, format="json")

    assert response.status_code == 200
    assert "access" in response.data
