import pytest
from domain.models import CustomUser

@pytest.mark.django_db
def test_custom_user_manager_hashes_password_on_creation():
    user = CustomUser.objects.create_user(
        email='luka@gmail.com',
        password='password123',
        first_name='Luka',
        last_name='Mania',
        role='Student'
    )

    assert user.check_password('password123')

@pytest.mark.django_db
def test_custom_user_manager_normalizes_email_on_creation():
    user = CustomUser.objects.create_user(
        email='luka@GMAil.cOM',
        password='password123',
        first_name='Luka',
        last_name='Mania',
        role='Student'
    )

    assert user.email == 'luka@gmail.com'
