from .base import UserRoleBasedPermission
from domain.models import GradeComment, CustomUser

class CanManageGradeComment(UserRoleBasedPermission):
    access_permitted_roles: list[CustomUser.Roles] = [CustomUser.Roles.TEACHER, CustomUser.Roles.STUDENT]

    def has_object_permission(self, request, view, obj: GradeComment) -> bool:
        user = request.user

        return (
            user == obj.author
            or
            super().has_object_permission(request, view, obj)
        )
