from rest_framework.permissions import BasePermission
from domain.models import CustomUser, Course

class CanManageCourse(BasePermission):
    access_permitted_roles: list[CustomUser.Roles] = [CustomUser.Roles.TEACHER] # allowed to - [GET, CREATE]
    modify_permitted_roles: list[CustomUser.Roles] = [] # allowed to [GET, CREATE, DELETE, PUT, PATCH]

    def has_permission(self, request, view) -> bool:
        return any(request.user.role == role.value for role in self.access_permitted_roles + self.modify_permitted_roles)

    def has_object_permission(self, request, view, obj: Course) -> bool:
        return (
            request.user == obj.lead
            or
            any(request.user.role == role.value for role in self.modify_permitted_roles)
        )
