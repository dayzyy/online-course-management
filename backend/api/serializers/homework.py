from rest_framework import serializers
from domain.models import Homework

class HomeworkInfoSerializer(serializers.ModelSerializer):
    lecture_id = serializers.IntegerField(source="lecture.id", read_only=True)

    class Meta:
        model = Homework
        fields = ["id", "content", "created_at", "due", "lecture_id"]

class HomeworkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ["content", "due", "lecture"]
        extra_kwargs = {
            "lecture": {"write_only": True}
        }
