from .base import UserRoleBasedPermission
from domain.models import CustomUser, Course

class CanManageCourse(UserRoleBasedPermission):
    access_permitted_roles: list[CustomUser.Roles] = [CustomUser.Roles.TEACHER]

    def has_object_permission(self, request, view, obj: Course) -> bool:
        return (
            request.user == obj.lead
            or
            super().has_object_permission(request, view, obj)
        )
