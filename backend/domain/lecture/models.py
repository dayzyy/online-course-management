from django.db import models
from domain.models import Course, CustomUser

class Lecture(models.Model):
    topic = models.CharField(max_length=255)
    presentation = models.FileField()
    held_at = models.DateTimeField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lectures'
    )

    # Allow this field to be null, so lectures can be created at first, and then assigned a teacher at any point of time
    teacher = models.ForeignKey(
        CustomUser,
        limit_choices_to={'role': CustomUser.Roles.TEACHER},
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='teaching_lessons'
    )
