from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from forum.models import ForumAccount


def user_permission(forum_element, account):
    """
        Checks if a user has the necessary permission to interact with a forum element.

        This function evaluates whether the specified account is either the owner of the forum element or has forum
        master status. If neither condition is met, it raises a PermissionDenied exception, indicating that the user
        does not have the required permissions to perform the action on the forum element.

        Args:
            forum_element: The forum element (e.g., topic, message) to check permissions against.
            account: The user's forum account being checked for permissions.

        Raises:
            PermissionDenied: If the account does not own the forum element and is not a forum master.
        """
    if forum_element.account != account and not account.forum_master:
        raise PermissionDenied()


def verify_active_forum_account(user, forum):
    """
        Verifies if a user has an active forum account for a specific forum.

        This function checks whether the given user has an active account associated with the specified forum. It returns
        True if such an account exists. If no active account is found, it raises a PermissionDenied exception, indicating
        that the user lacks the necessary permissions to access or perform actions within the forum.

        Args:
            user: The user whose forum account is being verified.
            forum: The forum in question.

        Returns:
            bool: True if an active forum account for the user exists in the specified forum.

        Raises:
            PermissionDenied: If no active forum account for the user exists in the specified forum.
        """
    try:
        ForumAccount.objects.get(user=user, forum=forum, active=True)
        return True
    except ObjectDoesNotExist:
        raise PermissionDenied()


def verify_forum_master_status(account):
    """
        Verifies if the provided account has forum master status.

        This function checks whether the given account has the status of a forum master. It returns True if the account
        is indeed a forum master. If the account does not have forum master status or if the account object does not
        have the necessary attributes (indicating an invalid account object), it raises a PermissionDenied exception.

        Args:
            account: The forum account being verified for forum master status.

        Returns:
            bool: True if the account is a forum master.

        Raises:
            PermissionDenied: If the account is not a forum master or if the account object is invalid.
        """
    try:
        if account.forum_master:
            return True
        else:
            raise PermissionDenied()
    except AttributeError:
        raise PermissionDenied()


def verify_account_for_private_conversation(account, conversation, contacts):
    """
       Verifies if a forum account has permission to access a private conversation.

       This function checks whether the given account is either the owner of the conversation or one of the contacts
       in a private conversation. If the account does not match either of these criteria, it raises a
       PermissionDenied exception, indicating that the user is not authorized to access the private conversation.

       Args:
           account: The forum account being verified for access.
           conversation: The private conversation object to check access against.
           contacts: A list of forum accounts that are participants in the conversation.

       Raises:
           PermissionDenied: If the account is neither the owner of the conversation nor a contact in the conversation.
       """
    if account != conversation.account and account not in contacts:
        raise PermissionDenied()
