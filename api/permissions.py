from rest_framework.permissions import BasePermission


class HasModelPerm(BasePermission):
    perm = None

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.has_perm(self.perm))
