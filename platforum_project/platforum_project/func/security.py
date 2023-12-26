from django.core.exceptions import PermissionDenied


def user_permission(forum_element, user):
    if forum_element.user != user:
        raise PermissionDenied()
