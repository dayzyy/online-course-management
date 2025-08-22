import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from domain.models import CustomUser

@pytest.mark.django_db
def test_custom_user_can_obtain_jwt_tokens():
    user = CustomUser.objects.create_user(
        'luka@gmail.com',
        'password123',
        'Luka',
        'Mania',
        'Student'
    )

    path = reverse('token_obtain_pair')

    client = APIClient()
    response = client.post(path, {"email": user.email, "password": "password123"}, format="json")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_custom_user_can_refresh_token():
    user = CustomUser.objects.create_user(
        'luka@gmail.com',
        'password123',
        'Luka',
        'Mania',
        'Student'
    )

    path = reverse('token_obtain_pair')

    client = APIClient()
    response = client.post(path, {"email": user.email, "password": "password123"}, format="json")

    refresh_token = response.data['refresh']

    path = reverse('token_refresh')
    response = client.post(path, {"refresh": refresh_token}, format="json")

    assert response.status_code == 200
    assert "access" in response.data
