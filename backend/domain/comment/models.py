from django.db import models
from domain.models import Grade, CustomUser

class Comment(models.Model):
    class Meta:
        abstract = True

    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    author = models.ForeignKey(
        CustomUser,
        limit_choices_to={'role': CustomUser.Roles.TEACHER},
        on_delete=models.CASCADE,
        related_name='comments'
    )

class GradeComment(Comment):
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name='comments'
    )
