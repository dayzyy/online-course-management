from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q
from domain.models import Submission, CustomUser
from api.serializers.submission import SubmissionInfoSerializer, SubmissionCreateSerializer
from api.permissions.submission import CanManageSubmission

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SubmissionInfoSerializer

        return SubmissionCreateSerializer

    def get_permissions(self):
        perms = [IsAuthenticated()]
        if self.action not in ['list', 'retrieve']:
            perms.append(CanManageSubmission())

        return perms

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset

        if user.role == CustomUser.Roles.STUDENT.value:
            qs = qs.filter(author=user)
        elif user.role == CustomUser.Roles.TEACHER.value:
            qs = qs.filter(
                Q(homework__lecture__teacher=user) |
                Q(homework__lecture__course__lead=user)
            ).distinct()

        homework_id = self.request.query_params.get("homework")
        if homework_id:
            qs = qs.filter(homework_id=homework_id)

        lecture_id = self.request.query_params.get("lecture")
        if lecture_id:
            qs = qs.filter(homework__lecture_id=lecture_id)

        return qs

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='homework',
                description='Filter submissions by homework ID',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='lecture',
                description='Filter submissions by lecture ID',
                required=False,
                type=int
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
