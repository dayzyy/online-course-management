from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from domain.models import Course
from api.serializers.course import CourseInfoSerializer, CourseCreateSerializer
from api.permissions.course import CanManageCourse

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, CanManageCourse]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseInfoSerializer

        return CourseCreateSerializer
