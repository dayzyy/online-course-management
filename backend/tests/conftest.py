import pytest
from domain.models import CustomUser

_DEFAULT_USER_PASSWORD = 'password123'

@pytest.fixture
def default_user(db) -> CustomUser:
    return CustomUser.objects.create_user(
        email='luka@gmail.com',
        password=_DEFAULT_USER_PASSWORD,
        first_name='Luka',
        last_name='Mania',
        role='Student'
    )

@pytest.fixture
def default_user_password() -> str:
    return _DEFAULT_USER_PASSWORD
