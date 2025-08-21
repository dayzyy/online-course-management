from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import fields, TextChoices

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, role):
        for field_semantic, value in [
            ('an email', email),
            ('a password', password),
            ('a first name', first_name),
            ('a last name', last_name),
            ('a role', role)
        ]:
            if not value:
                raise ValueError(f"User must provide {field_semantic}!")

        email = self.normalize_email(email)

        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)
        user.save(using=self._db)

        return user

class CustomUser(AbstractBaseUser):
    class Roles(TextChoices):
        TEACHER = 'Teacher'
        STUDENT = 'Student'

    email = fields.EmailField(unique=True)
    first_name = fields.CharField(max_length=20)
    last_name = fields.CharField(max_length=20)
    role = fields.CharField(max_length=20, choices=Roles.choices)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()
