from .base import UserRoleBasedPermission
from domain.models import Lecture, CustomUser

class CanManageLecture(UserRoleBasedPermission):
    access_permitted_roles: list[CustomUser.Roles] = [CustomUser.Roles.TEACHER]

    def has_permission(self, request, view) -> bool:
        return any(request.user.role == role.value for role in self.access_permitted_roles + self.modify_permitted_roles)

    def has_object_permission(self, request, view, obj: Lecture) -> bool:
        user = request.user

        if user == obj.course.lead:
            return True
        if user == obj.teacher:
            return True

        return super().has_object_permission(request, view, obj)
