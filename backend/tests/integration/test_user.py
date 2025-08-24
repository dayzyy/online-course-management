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

@pytest.mark.parametrize(
    "user_data, missing_fields",
    [
        (
            {"password": "Ex123!", "first_name": "Luka", "last_name": "Mania", "role": "Student"},
            ["email"]
        ),
        (
            {"email": "ex@gmail.com", "first_name": "Luka", "last_name": "Mania", "role": "Student"},
            ["password"]
        ),
        (
            {"email": "ex@gmail.com", "password": "Ex123!", "last_name": "Mania", "role": "Student"},
            ["first_name"]
        ),
        (
            {"email": "ex@gmail.com", "password": "Ex123!", "first_name": "Luka", "role": "Student"},
            ["last_name"]
        ),
        (
            {"email": "ex@gmail.com", "password": "Ex123!", "first_name": "Luka", "last_name": "Mania"},
            ["role"]
        ),
    ]
)
def test_register_fails_when_missing_fields(db, api_client: APIClient, user_data: dict, missing_fields: list[str]):
    path = reverse("register")
    response = api_client.post(path, user_data, format="json")

    assert response.status_code == 400

    for field in missing_fields:
        assert field in response.data

def test_register_fails_when_taken_email(api_client: APIClient, default_user: CustomUser):
    user_data = {
        "email": default_user.email,
        "password": "painHealsAll123",
        "first_name": "Fyodor",
        "last_name": "Dostoevsky",
        "role": CustomUser.Roles.STUDENT.value
    }

    path = reverse('register')
    response = api_client.post(path, user_data, format="json")

    assert response.status_code == 400
    assert "email" in response.data

def test_register_fails_when_invalid_role(db, api_client: APIClient):
    user_data = {
        "email": "ex@gmail.ru",
        "password": "notJustAPawn123",
        "first_name": "Rodion",
        "last_name": "Raskolnikov",
        "role": "Law Student"
    }

    path = reverse('register')
    response = api_client.post(path, user_data, format="json")

    assert response.status_code == 400
    assert f"Choose role from {[r[1] for r in CustomUser.Roles.choices]}" in response.data['role']
