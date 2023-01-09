from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


# class IsAdminOrReadOnly(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if request.user.is_authenticated:
#             return request.user.is_superuser or request.user.role in ('admin',)
#         return False

#     def has_object_permission(self, request, view, obj):
#         return request.user.is_superuser or request.user.role in ('admin',)
