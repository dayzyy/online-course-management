from django.db import models
from domain.models import Lecture

class Homework(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField()

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name='homeworks'
    )
