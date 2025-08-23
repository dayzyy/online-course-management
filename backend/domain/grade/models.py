from django.db import models
from domain.models import Homework, CustomUser

class Grade(models.Model):
    value = models.PositiveIntegerField()

    homework = models.OneToOneField(
        Homework,
        on_delete=models.CASCADE,
        related_name='grade'
    )

    grader = models.OneToOneField(
        CustomUser,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
