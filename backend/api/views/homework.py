from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter

from domain.models import Homework
from api.serializers.homework import HomeworkInfoSerializer, HomeworkCreateSerializer
from api.permissions.homework import CanManageHomework
from domain.user.models import CustomUser


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return HomeworkInfoSerializer
        return HomeworkCreateSerializer

    def get_permissions(self):
        perms = [IsAuthenticated()]
        if self.action not in ['list', 'retrieve']:
            perms.append(CanManageHomework())

        return perms

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset

        if user.role == CustomUser.Roles.STUDENT.value:
            qs = qs.filter(lecture__course__students=user)

        elif user.role == CustomUser.Roles.TEACHER.value:
            qs = qs.filter(
                Q(lecture__course__lead=user) |
                Q(lecture__teacher=user)
            ).distinct()

        course_id = self.request.query_params.get("course")
        if course_id:
            qs = qs.filter(lecture__course_id=course_id)

        lecture_id = self.request.query_params.get("lecture")
        if lecture_id:
            qs = qs.filter(lecture_id=lecture_id)

        return qs

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='course',
                description='Filter homework by course id',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='lecture',
                description='Filter homework by lecture id',
                required=False,
                type=int,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
