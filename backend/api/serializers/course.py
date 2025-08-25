from rest_framework import serializers
from domain.models import Course, CustomUser
from .user import UserInfoSerializer

class CourseInfoSerializer(serializers.ModelSerializer):
    lead = UserInfoSerializer(read_only=True)
    teachers = UserInfoSerializer(many=True, read_only=True)
    students = UserInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_at', 'lead', 'teachers', 'students']

class CourseCreateSerializer(serializers.ModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role=CustomUser.Roles.TEACHER.value)
    )
    teachers = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role=CustomUser.Roles.TEACHER.value),
        many=True,
        required=False,
    )
    students = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role=CustomUser.Roles.STUDENT.value),
        many=True,
        required=False,
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lead', 'teachers', 'students']
        extra_kwargs = {"id": {"read_only": True}}
