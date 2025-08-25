from rest_framework import serializers
from domain.models import Grade, Homework
from .user import UserInfoSerializer
from .homework import HomeworkInfoSerializer

class GradeInfoSerializer(serializers.ModelSerializer):
    grader = UserInfoSerializer(read_only=True)
    homework = HomeworkInfoSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = ["id", "value", "homework", "grader"]

class GradeCreateSerializer(serializers.ModelSerializer):
    homework = serializers.PrimaryKeyRelatedField(
        queryset=Homework.objects.all()
    )

    class Meta:
        model = Grade
        fields = ["id", "value", "homework"]
        extra_kwargs = {
            "id": {"read_only": True}
        }
