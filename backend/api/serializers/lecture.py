from rest_framework import serializers
from domain.models import Lecture, CustomUser
from .user import UserInfoSerializer
from .course import CourseInfoSerializer

class LectureInfoSerializer(serializers.ModelSerializer):
    course = CourseInfoSerializer(read_only=True)
    teacher = UserInfoSerializer(read_only=True)

    class Meta:
        model = Lecture
        fields = ['id', 'topic', 'presentation', 'held_at', 'course', 'teacher']


class LectureCreateSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role=CustomUser.Roles.TEACHER.value),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Lecture
        fields = ['topic', 'presentation', 'held_at', 'course', 'teacher']
