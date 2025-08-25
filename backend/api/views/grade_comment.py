from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from domain.models import GradeComment
from api.serializers.grade_comment import GradeCommentCreateSerializer, GradeCommentInfoSerializer
from api.permissions.grade_comment import CanManageGradeComment

class GradeCommentViewSet(viewsets.ModelViewSet):
    queryset = GradeComment.objects.all()

    def get_permissions(self):
        perms = [IsAuthenticated()]
        if self.action not in ['list', 'retrieve']:
            perms.append(CanManageGradeComment())

        return perms

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return GradeCommentCreateSerializer

        return GradeCommentInfoSerializer

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)
