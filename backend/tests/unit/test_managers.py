from domain.models import CustomUser

def test_custom_user_manager_hashes_password_on_creation(default_user: CustomUser, default_user_password: str):
    assert default_user.check_password(default_user_password)
    assert default_user.password != default_user_password

def test_custom_user_manager_normalizes_email_on_creation(db):
    user = CustomUser.objects.create_user(
        email="default@EXAMPLe.com",
        password="password123",
        first_name="Student",
        last_name="Example",
        role=CustomUser.Roles.STUDENT.value
    )

    assert user.email == 'default@example.com'
