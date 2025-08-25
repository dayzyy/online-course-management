from rest_framework.permissions import BasePermission
from domain.models import CustomUser, Submission
from django.utils import timezone

class CanManageSubmission(BasePermission):
    access_permitted_roles: list[CustomUser.Roles] = [CustomUser.Roles.STUDENT, CustomUser.Roles.TEACHER]
    modify_permitted_roles: list[CustomUser.Roles] = []

    def has_permission(self, request, view) -> bool:
        return any(request.user.role == role.value for role in self.access_permitted_roles + self.modify_permitted_roles)

    def has_object_permission(self, request, view, obj: Submission) -> bool:
        user = request.user

        if user == obj.author and timezone.now() < obj.homework.due:
            return True

        lecture = obj.homework.lecture

        if user == lecture.teacher:
            return True
        if user == lecture.course.lead:
            return True

        return any(user.role == role.value for role in self.modify_permitted_roles)
