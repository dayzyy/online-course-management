from django.db import models
from domain.models import Homework, CustomUser

class Submission(models.Model):
    content = models.TextField()
    attachment = models.FileField(null=True, blank=True)

    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Roles.STUDENT},
        related_name='submissions'
    )
