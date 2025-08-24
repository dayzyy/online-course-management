from rest_framework.permissions import BasePermission
from domain.models import CustomUser

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == CustomUser.Roles.TEACHER.value

class IsCourseLead(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.lead == request.user
