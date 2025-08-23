from django.db import models
from domain.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    lead = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Roles.TEACHER},
        related_name='leading_courses'
    )

    teachers = models.ManyToManyField(
        CustomUser,
        limit_choices_to={'role': CustomUser.Roles.TEACHER},
        related_name='teaching_courses'
    )

    students = models.ManyToManyField(
        CustomUser,
        limit_choices_to={'role': CustomUser.Roles.STUDENT},
    )
