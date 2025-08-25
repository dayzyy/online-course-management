from rest_framework.permissions import BasePermission
from domain.models import CustomUser, Grade

class CanManageGrade(BasePermission):
    access_permitted_roles = [CustomUser.Roles.TEACHER]
    modify_permitted_roles = []

    def has_permission(self, request, view) -> bool:
        return any(request.user.role == role.value for role in self.access_permitted_roles + self.modify_permitted_roles)

    def has_object_permission(self, request, view, obj: Grade) -> bool:
        user = request.user

        if user.role == CustomUser.Roles.TEACHER.value:
            lecture = obj.homework.lecture
            if user == lecture.teacher or user == lecture.course.lead:
                return True

        return any(request.user.role == role.value for role in self.modify_permitted_roles)
