from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from account.models import CustomUser
from platforum_project.func.security import user_permission, verify_active_forum_account
from forum.models import Forum, Category, SubCategory, Topic, Message, ForumAccount, Notification, Like
from forum.forms import CreateTopic, PostMessage


@login_required
def index(request, slug_forum, pk_forum):
    """
       Displays the main page of a specific forum.

       This view, accessible only to logged-in users, retrieves and displays the main page of a specified forum based on
       its primary key. It attempts to retrieve the user's account for this forum and, if found, updates the user's
       badges using the 'badges_manager' method. The view also fetches and displays all categories within the forum.
       If no account is associated with the user in this forum, the user's account details are not displayed.

       Args:
           request: The HTTP request object.
           slug_forum: The slug of the forum (unused in the function but required for URL pattern).
           pk_forum: The primary key of the forum.

       Returns:
           HttpResponse: Renders the main page of the forum with context data including the forum, its categories,
           and the user's forum account (if present).
       """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account: ForumAccount = user.retrieve_forum_account(forum)
    if account:
        account.badges_manager()
    categories = Category.objects.filter(forum=forum)
    return render(request, "forum/index.html", context={"forum": forum, "categories": categories, "account": account})


@login_required
def sub_category_view(request, pk, slug_forum, pk_forum, slug_sub_category):
    """
       Displays the topics within a specific sub-category of a forum.

       This view, available only to logged-in users, shows the topics under a particular sub-category of a forum. It
       lists both pinned and regular topics separately. The topics are paginated with 10 topics per page. The view
       retrieves the user's forum account for additional context, such as permissions or user-specific data.

       Args:
           request: The HTTP request object.
           pk: The primary key of the sub-category.
           slug_forum: The slug of the forum (unused in the function but required for URL pattern).
           pk_forum: The primary key of the forum.
           slug_sub_category: The slug of the sub-category (unused in the function but required for URL pattern).

       Returns:
           HttpResponse: Renders the sub-category page with context data including the sub-category, forum, topics,
           pinned topics, user's forum account, and pagination object.
       """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)
    topics = Topic.objects.filter(sub_category=sub_category, pin=False)
    pin_topics = Topic.objects.filter(sub_category=sub_category, pin=True)

    paginator = Paginator(topics, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "forum/sub-category.html", context={"sub_category": sub_category,
                                                               "forum": forum,
                                                               "topics": topics, "pin_topics": pin_topics,
                                                               "account": account, "page_obj": page_obj})


@login_required
def add_topic(request, slug_forum, pk_forum, pk, slug_sub_category):
    """
        Handles the creation of a new topic within a sub-category of a forum.

        Available only to logged-in users with an active forum account, this view provides a form for creating a new
        topic in a specified sub-category. Upon POST request with valid data, a new topic and its initial message are
        created and associated with the user's account and the sub-category. After successful topic creation, the user
        is redirected to the newly created topic page.

        Args:
            request: The HTTP request object, either GET for displaying the form or POST for submitting form data.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.
            pk: The primary key of the sub-category.
            slug_sub_category: The slug of the sub-category (unused in the function but required for URL pattern).

        Returns:
            HttpResponse: Renders the new topic creation page with context data including the forum, sub-category, form,
            and user's forum account. Redirects to the new topic page upon successful creation.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)

    if request.method == "POST":
        form = CreateTopic(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.account = account
            topic.sub_category = sub_category
            topic.save()
            Message.objects.create(message=form.cleaned_data["message"], account=account, topic=topic)
            return redirect(topic)

    else:
        form = CreateTopic()
    return render(request, "forum/new-topic.html", context={
        "forum": forum,
        "sub_category": sub_category,
        "form": form, "account": account
    })


@login_required
def topic_view(request, slug_forum, pk_forum, pk, slug_sub_category, pk_topic, slug_topic):
    """
        Displays a specific forum topic and its messages.

        This view, accessible to logged-in users, presents the details of a specific topic, including all associated
        messages. The messages are paginated with 10 messages per page. It also provides a form for posting new messages
        to the topic. Upon POST request with valid data, a new message is added to the topic, and a notification is
        possibly sent to members following the topic.

        Args:
            request: The HTTP request object, either GET for displaying the topic and messages or POST for submitting
                     a new message.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.
            pk: The primary key of the sub-category.
            slug_sub_category: The slug of the sub-category (unused in the function but required for URL pattern).
            pk_topic: The primary key of the topic.
            slug_topic: The slug of the topic (unused in the function but required for URL pattern).

        Returns:
            HttpResponse: Renders the topic page with context data including the forum, sub-category, topic, messages,
            user's account, message posting form, and pagination object.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)
    topic = get_object_or_404(Topic, pk=pk_topic)
    messages = Message.objects.filter(topic=topic)

    paginator = Paginator(messages, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        verify_active_forum_account(user, forum)
        form = PostMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.topic = topic
            message.account = account
            message.save()
            Notification.notify_member_if_message_posted_in_topic(topic, account)
            return redirect(topic)
    else:
        form = PostMessage()
    return render(request, "forum/topic.html", context={
        "forum": forum,
        "sub_category": sub_category,
        "topic": topic,
        "messages": messages,
        "account": account,
        "form": form,
        "page_obj": page_obj
    })


@login_required
def like_unlike_view(request, pk_forum, pk_message):
    """
        Handles liking or unliking a forum message.

        This view, available to logged-in users with an active account in the forum, allows a user to toggle the like
        status of a message. It first verifies the user's active forum account, then uses the 'Like.like_unlike' method
        to either add or remove a like from the message, depending on the current like status. After toggling the like
        status, the user is redirected back to the topic containing the message.

        Args:
            request: The HTTP request object.
            pk_forum: The primary key of the forum.
            pk_message: The primary key of the message to be liked or unliked.

        Returns:
            HttpResponse: Redirects to the topic page that contains the message.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    message = get_object_or_404(Message, pk=pk_message)
    Like.like_unlike(liker=account, message=message)
    return redirect(message.topic)


@login_required
def update_message(request, slug_forum, pk_forum, pk, slug_sub_category, pk_topic, slug_topic, pk_message):
    """
        Handles the updating of a specific message within a forum topic.

        This view allows logged-in users to edit their own messages or messages in forums where they have an active
        account. It first verifies the user's active account status in the forum and checks if the user has permission
        to edit the message. A form is provided to edit the message, and upon submission with valid data, the message
        is updated. After updating, the user is redirected back to the topic.

        Args:
            request: The HTTP request object, either GET for displaying the edit form or POST for submitting the updated message.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.
            pk: The primary key of the sub-category.
            slug_sub_category: The slug of the sub-category (unused in the function but required for URL pattern).
            pk_topic: The primary key of the topic.
            slug_topic: The slug of the topic (unused in the function but required for URL pattern).
            pk_message: The primary key of the message to be updated.

        Returns:
            HttpResponse: Renders the message update page with context data including the forum, topic, sub-category,
            message, form, and user's account.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)
    topic = get_object_or_404(Topic, pk=pk_topic)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    message = get_object_or_404(Message, pk=pk_message)
    user_permission(message, account)

    if request.method == "POST":
        form = PostMessage(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect(topic)
    else:
        form = PostMessage(instance=message)
    return render(request, "forum/update-message.html", context={
        "forum": forum,
        "topic": topic,
        "message": message,
        "form": form,
        "sub_category": sub_category,
        "account": account
    })


@login_required
@require_POST
def delete_message(request, pk_forum, pk_topic, pk_message):
    """
       Handles the deletion of a specific message within a forum topic.

       This view allows logged-in users to delete their own messages or messages in forums where they have an active
       account. It first verifies the user's active account status in the forum and checks if the user has permission
       to delete the message. If authorized, the message is deleted, and the user is redirected back to the topic
       containing the deleted message.

       Args:
           request: The HTTP request object for message deletion (POST request).
           pk_forum: The primary key of the forum.
           pk_topic: The primary key of the topic.
           pk_message: The primary key of the message to be deleted.

       Returns:
           HttpResponse: Redirects to the topic page containing the deleted message.
       """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    message = get_object_or_404(Message, pk=pk_message)
    user_permission(message, account)
    message.delete()
    return redirect(Topic.objects.get(pk=pk_topic))


@login_required
def members_list_view(request, slug_forum, pk_forum):
    """
        Displays a list of active forum members.

        This view allows logged-in users to view a list of active members in a forum. It first verifies the user's
        active account status in the forum. Users can also perform a search to filter members by username.

        Args:
            request: The HTTP request object.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.

        Returns:
            HttpResponse: Renders the members list page with context data including the forum, user's account, and
            the list of active members.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    members = ForumAccount.objects.filter(forum=forum, active=True)

    search = request.GET.get("search")
    if search:
        members = ForumAccount.objects.filter(forum=forum, user__username__icontains=search)
    return render(request, "forum/members-list.html", context={"forum": forum,
                                                               "account": account, "members": members})


@login_required
def member_view(request, slug_forum, pk_forum, pk_member):
    """
        Displays the profile and activity of a forum member.

        This view allows logged-in users to view the profile and recent activity of a specific forum member. It first
        verifies the user's active account status in the forum and retrieves the member's profile and recent messages.

        Args:
            request: The HTTP request object.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.
            pk_member: The primary key of the forum member to view.

        Returns:
            HttpResponse: Renders the member's profile page with context data including the forum, user's account,
            the member's profile, and recent messages.
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    member = get_object_or_404(ForumAccount, pk=pk_member)
    last_messages = Message.objects.filter(account=member, topic__sub_category__category__forum=forum).order_by(
        "-creation")[:5]
    return render(request, "forum/member.html", context={"forum": forum, "account": account,
                                                         "member": member, "messages": last_messages})


@login_required
def query_view(request, slug_forum, pk_forum):
    """
        Displays search results for topics and messages within a forum.

        This view allows logged-in users to search for topics and messages within a forum based on a user's query.
        It first verifies the user's active account status in the forum and then performs the search for topics and messages
        matching the query.

        Args:
            request: The HTTP request object.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.

        Returns:
            HttpResponse: Renders the search results page with context data including the forum, user's account,
            search results for topics and messages.
        """
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)

    search = request.GET.get("query")
    if search:
        topics = Topic.objects.filter(title__icontains=search)
        messages = Message.objects.filter(
            Q(personal=False),
            Q(message__icontains=search) | Q(topic__title__icontains=search)
        )

    else:
        return redirect("forum:index", slug_forum=forum.slug, pk_forum=forum.pk)
    return render(request, "search/request.html", context={"forum": forum, "account": account,
                                                           "topics": topics, "messages": messages, "search": search})
