from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorUser(BasePermission):


    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True


        return (
                request.user.is_authenticated
                and hasattr(request.user, "profile")
                and request.user.profile.role == "author"
        )


class IsNormalUser(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "normal"
        )
