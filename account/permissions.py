from rest_framework.permissions import BasePermission


class IsGuardian(BasePermission):

    message = "User needs to be a guardian to access this view."

    def has_permission(self, request, view):
        """
        Checks whether the requesting user is a child or a guardian.
        """
        if request.user.user_type == "guardian":
            return True
        return False


class IsVerified(BasePermission):

    message = "User needs to be verified to access this view."

    def has_permission(self, request, view):
        """
        Checks whether a given user has permission.
        """
        if request.user.is_verified:
            return True
        return False
