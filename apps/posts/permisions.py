from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Only owner of object"""

    message = "You must be owner of this like."

    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.id
