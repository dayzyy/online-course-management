from rest_framework import serializers
from domain.models import Submission, Homework, CustomUser
from .user import UserInfoSerializer
from .homework import HomeworkInfoSerializer

class SubmissionInfoSerializer(serializers.ModelSerializer):
    student = UserInfoSerializer(read_only=True)
    homework = HomeworkInfoSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'content', 'attachment', 'homework', 'student']


class SubmissionCreateSerializer(serializers.ModelSerializer):
    homework = serializers.PrimaryKeyRelatedField(
        queryset=Homework.objects.all()
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role=CustomUser.Roles.STUDENT.value)
    )

    class Meta:
        model = Submission
        fields = ['id', 'content', 'attachment', 'homework', 'student']
        extra_kwargs = {"id": {"read_only": True}}
