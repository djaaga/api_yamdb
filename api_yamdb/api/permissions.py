from rest_framework import permissions


class ReviewPermission(permissions.BasePermission):
    """
    Предоставление прав доступа на изменение
    отзывов и комментариев.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
