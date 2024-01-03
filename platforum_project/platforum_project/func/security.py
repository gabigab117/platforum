from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from forum.models import ForumAccount


def user_permission(forum_element, user):
    if forum_element.user != user:
        raise PermissionDenied()


def user_has_active_forum_account(user, forum):
    try:
        account = ForumAccount.objects.get(user=user, forum=forum, active=True)
        return account
    except ObjectDoesNotExist:
        raise PermissionDenied()
