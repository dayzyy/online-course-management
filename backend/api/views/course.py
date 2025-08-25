from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q
from rest_framework.views import Response
from domain.models import Course, CustomUser
from api.serializers.course import CourseInfoSerializer, CourseCreateSerializer
from api.permissions.course import CanManageCourse

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseInfoSerializer

        return CourseCreateSerializer

    def get_permissions(self):
        perms = [IsAuthenticated()]
        if self.action not in ['list', 'retrieve']:
            perms.append(CanManageCourse())
        
        return perms

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset

        if user.role == CustomUser.Roles.TEACHER.value:
            view_type = self.request.query_params.get('view')
            if view_type == 'lead':
                return qs.filter(lead=user)
            if view_type == 'teaching':
                return qs.filter(teachers=user)

            return qs.filter(Q(lead=user) | Q(teachers=user)).distinct()

        if user.role == CustomUser.Roles.STUDENT.value:
            return qs.filter(students=user)

        return qs

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='view',
                description='Filter courses for teachers: "lead" = courses they lead, "teaching" = courses they teach',
                required=False,
                type=str,
                enum=['lead', 'teaching']
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(lead=self.request.user)

    @action(detail=True, methods=['POST'], url_path='add-members')
    def add_members(self, request, pk=None):
        course = self.get_object()
        teacher_ids = request.data.get("teachers", [])
        student_ids = request.data.get("students", [])

        if teacher_ids:
            teachers = CustomUser.objects.filter(id__in=teacher_ids)
            course.teachers.add(*teachers)

        if student_ids:
            students = CustomUser.objects.filter(id__in=student_ids)
            course.students.add(*students)

        return Response({"detail": "Members added successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='remove-members')
    def remove_members(self, request, pk=None):
        course = self.get_object()

        teacher_ids = request.data.get("teachers", [])
        student_ids = request.data.get("students", [])

        if teacher_ids:
            teachers = CustomUser.objects.filter(id__in=teacher_ids)
            course.teachers.remove(*teachers)

        if student_ids:
            students = CustomUser.objects.filter(id__in=student_ids)
            course.students.remove(*students)

        return Response({"detail": "Members removed successfully"}, status=status.HTTP_200_OK)
