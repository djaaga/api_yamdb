from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Полный доступ администраторам
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role == "admin" or request.user.is_staff)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ для просмотра
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role == "admin" or request.user.is_staff)
        )


class IsAdminOrAuthor(permissions.BasePermission):
    """
    Доступ для безопасных методов админу и автору
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.method in ("PATCH", "DELETE") and (
            request.user
            and (
                (
                    request.user.role in ("admin", "moderator")
                    or request.user.is_staff
                )
                or obj.author == request.user
            )
        )
