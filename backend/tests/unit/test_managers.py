import pytest
from domain.models import CustomUser

@pytest.mark.django_db
def test_custom_user_manager_hashes_password_on_creation():
    user = CustomUser.objects.create_user(
        'luka@gmail.com',
        'password123',
        'Luka',
        'Mania',
        'Student'
    )

    assert user.check_password('password123')

@pytest.mark.django_db
def test_custom_user_manager_normalizes_email_on_creation():
    user = CustomUser.objects.create_user(
        'luka@GMAil.cOM',
        'password123',
        'Luka',
        'Mania',
        'Student'
    )

    assert user.email == 'luka@gmail.com'
