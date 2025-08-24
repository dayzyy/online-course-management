from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from domain.models import Lecture
from api.serializers.lecture import LectureInfoSerializer, LectureCreateSerializer
from api.permissions.lecture import CanManageLecture
from domain.user.models import CustomUser

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LectureInfoSerializer

        return LectureCreateSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]

        return [IsAuthenticated(), CanManageLecture()]

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset

        if user.role == CustomUser.Roles.STUDENT.value:
            return qs.filter(course__students=user)

        if user.role == CustomUser.Roles.TEACHER.value:
            return qs.filter(Q(course__lead=user) | Q(teacher=user)).distinct()

        return qs
