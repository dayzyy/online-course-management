from .base import UserRoleBasedPermission
from domain.models import CustomUser, Grade

class CanManageGrade(UserRoleBasedPermission):
    access_permitted_roles = [CustomUser.Roles.TEACHER]

    def has_object_permission(self, request, view, obj: Grade) -> bool:
        user = request.user

        if user.role == CustomUser.Roles.TEACHER.value:
            lecture = obj.homework.lecture
            if user == lecture.teacher or user == lecture.course.lead:
                return True

        return super().has_object_permission(request, view, obj)
