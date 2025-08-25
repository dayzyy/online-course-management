from .base import UserRoleBasedPermission
from domain.models import Homework, CustomUser

class CanManageHomework(UserRoleBasedPermission):
    access_permitted_roles: list[CustomUser.Roles] = [CustomUser.Roles.TEACHER]

    def has_object_permission(self, request, view, obj: Homework) -> bool:
        user = request.user

        if user == obj.lecture.teacher:
            return True
        if user == obj.lecture.course.lead:
            return True

        return super().has_object_permission(request, view, obj)
