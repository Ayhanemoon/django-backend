from rest_framework import permissions


class IsOwnerOfAddress(permissions.BasePermission):
    """
    Custom permission to only allow owners of an address to access or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming the Address model has a 'profile' field that links to the Profile model,
        # and Profile has a 'user' field that links to the User model.
        return obj.profile == getattr(request.user, "profile", None)
