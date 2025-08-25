from rest_framework.permissions import BasePermission
from domain.models import GradeComment, CustomUser

class CanManageGradeComment(BasePermission):
    access_permitted_roles: list[CustomUser.Roles] = [CustomUser.Roles.TEACHER, CustomUser.Roles.STUDENT]
    modify_permitted_roles: list[CustomUser.Roles] = []  

    def has_permission(self, request, view) -> bool:
        return any(request.user.role == role.value for role in self.access_permitted_roles + self.modify_permitted_roles)

    def has_object_permission(self, request, view, obj: GradeComment) -> bool:
        user = request.user

        return (
            user == obj.author
            or
            any(user.role == role.value for role in self.modify_permitted_roles)
        )
