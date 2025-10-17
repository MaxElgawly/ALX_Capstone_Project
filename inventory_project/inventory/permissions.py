from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only to anyone, but write only to the owner.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE methods allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # write allowed only to owner
        return obj.owner == request.user
