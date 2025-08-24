import pytest
from domain.models import CustomUser
from rest_framework.test import APIClient

_DEFAULT_USER_PASSWORD = 'password123'

@pytest.fixture
def default_user(db) -> CustomUser:
    return CustomUser.objects.create_user(
        email='luka@gmail.com',
        password=_DEFAULT_USER_PASSWORD,
        first_name='Luka',
        last_name='Mania',
        role=CustomUser.Roles.STUDENT.value
    )

@pytest.fixture
def default_user_password() -> str:
    return _DEFAULT_USER_PASSWORD

@pytest.fixture()
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def teacher_user(db):
    return CustomUser.objects.create_user(
        email="teacher@example.com",
        password="password123",
        first_name="Teacher",
        last_name="Example",
        role=CustomUser.Roles.TEACHER.value
    )

@pytest.fixture
def student_user(db):
    return CustomUser.objects.create_user(
        email="student@example.com",
        password="password123",
        first_name="Student",
        last_name="Example",
        role=CustomUser.Roles.STUDENT.value
    )
