from rest_framework.permissions import BasePermission

class IsEducator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='Educators').exists()
        )
