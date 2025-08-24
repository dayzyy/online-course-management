from rest_framework.permissions import BasePermission
from domain.models import Homework, CustomUser

class CanManageHomework(BasePermission):
    access_permitted_roles: list[CustomUser.Roles] = [CustomUser.Roles.TEACHER]
    modify_permitted_roles: list[CustomUser.Roles] = []

    def has_permission(self, request, view) -> bool:
        return any(request.user.role == role.value for role in self.access_permitted_roles + self.modify_permitted_roles)

    def has_object_permission(self, request, view, obj: Homework) -> bool:
        user = request.user

        if user == obj.lecture.teacher:
            return True
        if user == obj.lecture.course.lead:
            return True
        if any(user.role == role.value for role in self.modify_permitted_roles):
            return True

        return False
