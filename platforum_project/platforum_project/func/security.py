from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from forum.models import ForumAccount


def user_permission(forum_element, account):
    if forum_element.account != account:
        raise PermissionDenied()


def verify_active_forum_account(user, forum):
    try:
        ForumAccount.objects.get(user=user, forum=forum, active=True)
        return True
    except ObjectDoesNotExist:
        raise PermissionDenied()
