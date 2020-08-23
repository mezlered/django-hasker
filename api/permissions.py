from rest_framework import permissions


class IsOwnerOfQuestionOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, answer):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `user`.
        return answer.question.author == request.user