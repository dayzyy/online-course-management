from rest_framework.permissions import BasePermission
from domain.models import Lecture, CustomUser

class CanManageLecture(BasePermission):
    access_permitted_roles = [CustomUser.Roles.TEACHER]
    modify_permitted_roles = []  

    def has_permission(self, request, view) -> bool:
        return any(request.user.role == role.value for role in self.access_permitted_roles + self.modify_permitted_roles)

    def has_object_permission(self, request, view, obj: Lecture) -> bool:
        user = request.user

        if user == obj.course.lead:
            return True
        if user == obj.teacher:
            return True
        if any(user.role == role.value for role in self.modify_permitted_roles):
            return True

        return False
