from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from account.models import CustomUser
from platforum_project.func.security import user_permission, verify_active_forum_account
from forum.models import Forum, Category, SubCategory, Topic, Message, ForumAccount, Notification
from forum.forms import CreateTopic, PostMessage


@login_required
def index(request, slug_forum, pk_forum):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    categories = Category.objects.filter(forum=forum)
    return render(request, "forum/index.html", context={"forum": forum, "categories": categories, "account": account})


@login_required
def sub_category_view(request, pk, slug_forum, pk_forum, slug_sub_category):
    # Afficher la liste des sujets (pagination)
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
def update_message(request, slug_forum, pk_forum, pk, slug_sub_category, pk_topic, slug_topic, pk_message):
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
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    member = get_object_or_404(ForumAccount, pk=pk_member)
    last_messages = Message.objects.filter(account=member, topic__sub_category__category__forum=forum).order_by(
        "-creation")[:5]
    return render(request, "forum/member.html", context={"forum": forum, "account": account,
                                                         "member": member, "messages": last_messages})
