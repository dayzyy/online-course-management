from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

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
            return qs.filter(lecture__course__students=user)

        if user.role == CustomUser.Roles.TEACHER.value:
            return qs.filter(Q(lecture__course__lead=user) | Q(lecture__teacher=user)).distinct()

        return qs
