from rest_framework import serializers
from domain.models import Submission, Homework
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
    author = UserInfoSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'content', 'attachment', 'homework', 'author']
        extra_kwargs = {"id": {"read_only": True}}
