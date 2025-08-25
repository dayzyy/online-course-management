from rest_framework import serializers
from domain.models import GradeComment
from .user import UserInfoSerializer

class GradeCommentInfoSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)

    class Meta:
        model = GradeComment
        fields = ['id', 'content', 'created_at', 'author', 'grade']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'grade': {'read_only': True}
        }

class GradeCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeComment
        fields = ['id', 'content', 'grade']
        extra_kwargs = {
            'id': {'read_only': True}
        }
