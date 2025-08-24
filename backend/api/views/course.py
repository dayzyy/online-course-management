from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q
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

        # Students can optionally see all courses
        if user.role == CustomUser.Roles.STUDENT.value:
            if self.request.query_params.get('all') == 'true':
                return qs
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
            OpenApiParameter(
                name='all',
                description='For students: show all courses instead of only enrolled ones',
                required=False,
                type=bool
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
