from domain.models import CustomUser

def test_custom_user_manager_hashes_password_on_creation(default_user: CustomUser, default_user_password: str):
    assert default_user.check_password(default_user_password)

def test_custom_user_manager_normalizes_email_on_creation(default_user: CustomUser):
    assert default_user.email == 'luka@gmail.com'
