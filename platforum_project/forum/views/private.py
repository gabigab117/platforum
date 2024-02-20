from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction

from account.models import CustomUser
from forum.models import Conversation, Forum, Message, ForumAccount, Notification
from forum.forms import PostMessage, ProfileUpdateForm, SignupForumForm, ConversationForm

from platforum_project.func.security import user_permission, verify_active_forum_account, \
    verify_account_for_private_conversation


@login_required
def signup_forum(request, slug_forum, pk_forum):
    """
    Handles user registration for a specific forum.

    This view allows a logged-in user to sign up for a particular forum. If the user is already a member of the forum,
    they are redirected to their forum profile. Otherwise, they can complete the forum-specific registration form.

    Args:
        request: The HTTP request object.
        slug_forum: The slug of the forum.
        pk_forum: The primary key of the forum.

    Returns:
        HttpResponse: Renders the forum registration page or redirects to the user's forum profile if registration is
        successful or if the user is already a member.
    """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    if account:
        return redirect("forum:profile", pk_forum=forum.pk, slug_forum=forum.slug)

    if request.method == "POST":
        form = SignupForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum_account = form.save(commit=False)
            forum_account.forum = forum
            forum_account.user = user
            forum_account.save()
            return redirect("forum:profile", pk_forum=forum.pk, slug_forum=forum.slug)
    else:
        form = SignupForumForm()
    return render(request, "private/signup.html", context={"form": form, "forum": forum, "account": account})


@login_required
def start_conversation(request, slug_forum, pk_forum, pk_member):
    """
    Starts a private conversation with another forum member.

    This view allows a logged-in user to initiate a private conversation with another member of the forum.
    The user selects a forum member, enters a message, and starts the conversation.

    Args:
        request: The HTTP request object.
        slug_forum: The slug of the forum.
        pk_forum: The primary key of the forum.
        pk_member: The primary key of the forum member with whom the conversation is initiated.

    Returns:
        HttpResponse: Renders the private conversation initiation page or redirects to the conversation
        if the initiation is successful.
    """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    member = get_object_or_404(ForumAccount, pk=pk_member)

    if request.method == "POST":
        form = ConversationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                conversation = form.save(commit=False)
                conversation.account = account
                conversation.forum = forum
                conversation.save()
                conversation.contacts.add(member)
                Message.objects.create(message=form.cleaned_data["message"], account=account, conversation=conversation,
                                       personal=True)
            return redirect(conversation)
    else:
        form = ConversationForm()
    return render(request, "private/start-conversation.html",
                  context={"forum": forum, "account": account, "member": member,
                           "form": form})


@login_required
def personal_messaging(request, slug_forum, pk_forum):
    """
    Displays the personal messaging interface for a forum user.

    This view allows a logged-in user to access their personal messaging interface within a forum. It lists the user's
    own conversations and conversations they are a part of.

    Args:
        request: The HTTP request object.
        slug_forum: The slug of the forum.
        pk_forum: The primary key of the forum.

    Returns:
        HttpResponse: Renders the personal messaging interface page with context data including the user's conversations
         and forum details.
    """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    my_conversations = Conversation.objects.filter(forum=forum, account=account)
    conversations = Conversation.objects.filter(forum=forum, contacts=account)
    return render(request, "private/personal-messaging.html", context={
        "forum": forum,
        "my_conversations": my_conversations, "conversations": conversations, "account": account
    })


@login_required
def conversation_view(request, slug_forum, pk_forum, slug_conversation, pk_conversation):
    """
        Render and handle private conversation view.

        This view renders the private conversation page, allowing users to view and post messages in a private conversation.
        It verifies the user's active forum account, checks permissions to access the conversation, and handles message posting.

        Args:
            request: The HTTP request object.
            slug_forum: The slug of the forum.
            pk_forum: The primary key of the forum.
            slug_conversation: The slug of the conversation.
            pk_conversation: The primary key of the conversation.

        Returns:
            HttpResponse: Renders the private conversation page with context data.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    conversation = get_object_or_404(Conversation, pk=pk_conversation)
    account = user.retrieve_forum_account(forum)
    messages = Message.objects.filter(conversation=conversation)
    contacts = conversation.contacts.all()

    paginator = Paginator(messages, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    verify_account_for_private_conversation(account, conversation, contacts)

    if request.method == "POST":
        form = PostMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation, message.account, message.personal = conversation, account, True
            message.save()
            Notification.notify_member_if_message_posted_in_conversation(conversation, account)
            return redirect(conversation)
    else:
        form = PostMessage()
    return render(request, "private/conversation.html",
                  context={"account": account, "forum": forum, "conversation": conversation, "messages": messages,
                           "form": form, "contacts": contacts, "page_obj": page_obj})


@login_required
def update_message_conversation(request, slug_forum, pk_forum, slug_conversation, pk_conversation, pk_message):
    """
       Render and handle the update of a message within a private conversation.

       This view renders the message update form within a private conversation and handles the message update process.
       It verifies the user's active forum account, checks permissions to update the message, and updates the message content.

       Args:
           request: The HTTP request object.
           slug_forum: The slug of the forum.
           pk_forum: The primary key of the forum.
           slug_conversation: The slug of the conversation.
           pk_conversation: The primary key of the conversation.
           pk_message: The primary key of the message to be updated.

       Returns:
           HttpResponse: Renders the message update form with context data.
       """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    conversation = get_object_or_404(Conversation, pk=pk_conversation)
    message = get_object_or_404(Message, pk=pk_message)
    user_permission(message, account)

    if request.method == "POST":
        form = PostMessage(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect(conversation)
    else:
        form = PostMessage(instance=message)
    return render(request, "private/update-message.html", context={"forum": forum, "form": form,
                                                                   "conversation": conversation, "account": account})


@require_POST
@login_required
def delete_message_conversation(request, pk_forum, pk_conversation, pk_message):
    """
        Handle the deletion of a message within a private conversation.

        This view handles the deletion of a message within a private conversation. It verifies the user's active forum account,
        checks permissions to delete the message, and deletes the message from the conversation.

        Args:
            request: The HTTP request object.
            pk_forum: The primary key of the forum.
            pk_conversation: The primary key of the conversation.
            pk_message: The primary key of the message to be deleted.

        Returns:
            HttpResponse: Redirects back to the conversation after deleting the message.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    conversation = get_object_or_404(Conversation, pk=pk_conversation)
    message = get_object_or_404(Message, pk=pk_message)
    user_permission(message, account)
    message.delete()
    return redirect(conversation)


@login_required
def profile_forum(request, slug_forum, pk_forum):
    """
        Display and update the user's forum profile.

        This view allows users to view and update their forum profile information. It retrieves the user's forum account,
        displays their profile details, and allows them to update avatar.

        Args:
            request: The HTTP request object.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.

        Returns:
            HttpResponse: Renders the user's profile page with the ability to update profile information.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    last_messages = Message.objects.filter(account=account, topic__sub_category__category__forum=forum).order_by(
        "-creation")[:5]

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
            return redirect(request.path)
    else:
        form = ProfileUpdateForm()
    return render(request, "private/profile.html", context={"forum": forum, "account": account, "form": form,
                                                            "messages": last_messages})


@login_required
def notifications_view(request, slug_forum, pk_forum):
    """
       Display a user's forum notifications.

       This view allows users to view their forum notifications. It retrieves the user's forum account and
       displays their notifications.

       Args:
           request: The HTTP request object.
           slug_forum: The slug of the forum (unused in the function but required for URL pattern).
           pk_forum: The primary key of the forum.

       Returns:
           HttpResponse: Renders the user's notifications page with a list of notifications.
       """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    notifications = Notification.objects.filter(account=account)
    return render(request, "private/notifications.html", context={"forum": forum, "account": account,
                                                                  "notifications": notifications})


@login_required
@require_POST
def delete_notifications(request, pk_forum):
    """
        Delete a user's forum notifications.

        This view allows users to delete all of their forum notifications.
        It retrieves the user's forum account, deletes all notifications, resets the notification counter, and redirects
        to the notifications page.

        Args:
            request: The HTTP request object.
            pk_forum: The primary key of the forum.

        Returns:
            HttpResponse: Redirects to the user's notifications page after deleting all notifications.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account: ForumAccount = user.retrieve_forum_account(forum)
    Notification.objects.filter(account=account).delete()
    account.notification_counter = 0
    account.save()
    return redirect("forum:alerts", slug_forum=forum.slug, pk_forum=forum.pk)
