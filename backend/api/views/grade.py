from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q
from domain.models import Grade, CustomUser
from api.serializers.grade import GradeInfoSerializer, GradeCreateSerializer
from api.permissions.grade import CanManageGrade

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GradeInfoSerializer

        return GradeCreateSerializer

    def get_permissions(self):
        perms = [IsAuthenticated()]
        if self.action not in ['list', 'retrieve']:
            perms.append(CanManageGrade())
        
        return perms

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset

        if user.role == CustomUser.Roles.STUDENT.value:
            qs = qs.filter(homework__lecture__course__students=user)
        elif user.role == CustomUser.Roles.TEACHER.value:
            qs = qs.filter(
                Q(homework__lecture__teacher=user) |
                Q(homework__lecture__course__lead=user)
            )

        course_id = self.request.query_params.get('course')
        if course_id:
            qs = qs.filter(homework__lecture__course__id=course_id)

        return qs.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='course',
                description='Filter grades for a specific course by ID',
                required=False,
                type=int
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(grader=self.request.user)
