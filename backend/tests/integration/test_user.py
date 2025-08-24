import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from domain.models import CustomUser

def test_register_success(db, api_client: APIClient):
    user_data = {
        "email": "example@gmail.ru",
        "password": "painHealsAll123",
        "first_name": "Fyodor",
        "last_name": "Dostoevsky",
        "role": CustomUser.Roles.TEACHER.value
    }

    path = reverse('register')
    response = api_client.post(path, user_data, format="json")

    assert response.status_code == 201
    assert CustomUser.objects.filter(email=user_data['email']).exists()
