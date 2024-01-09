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


def verify_forum_master_status(account):
    try:
        if account.forum_master:
            return True
        else:
            raise PermissionDenied()
    except AttributeError:
        raise PermissionDenied()


def verify_account_for_private_conversation(account, conversation, contacts):
    if account != conversation.account and account not in contacts:
        raise PermissionDenied()
