from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class CommentOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return super().has_permission(request, view) and request.user == comment.user


#
# class IsAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         return request.user.is_authenticated and request.user.role == 'admin'
#
#
# class IsUserAndOwner(BasePermission):
#     def has_permission(self, request, view, obj):
#         return request.user.role == 'user' and obj.user == request.user
#
# class IsCandidateAndCommentOwner(BasePermission):
#     def has_permission(self, request, view, obj):
#         return request.user.role == 'candidate' and obj.user == request.user
#