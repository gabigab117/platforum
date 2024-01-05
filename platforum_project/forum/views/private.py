from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from account.models import CustomUser
from forum.models import Conversation, Forum, ForumAccount, Message
from forum.forms import PostMessage, ProfileUpdateForm, SignupForumForm

from platforum_project.func.security import user_permission, verify_active_forum_account


@login_required
def signup_forum(request, slug_forum, pk_forum):
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, slug=slug_forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)

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
def personal_messaging(request, slug_forum, pk_forum):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    my_conversations = Conversation.objects.filter(forum=forum, user=user)
    conversations = Conversation.objects.filter(forum=forum, contacts=user)
    return render(request, "private/personal-messaging.html", context={
        "forum": forum,
        "my_conversations": my_conversations, "conversations": conversations, "account": account
    })


@login_required
def conversation_view(request, slug_forum, pk_forum, slug_conversation, pk_conversation):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    conversation = get_object_or_404(Conversation, pk=pk_conversation)
    account = user.retrieve_forum_account(forum)
    messages = Message.objects.filter(conversation=conversation)
    contacts = conversation.contacts.all()

    if user != conversation.user and user not in contacts:
        raise PermissionDenied()

    if request.method == "POST":
        verify_active_forum_account(user, forum)
        form = PostMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation, message.user, message.personal = conversation, user, True
            message.save()
            return redirect(conversation)
    else:
        form = PostMessage()
    return render(request, "private/conversation.html",
                  context={"account": account, "forum": forum, "conversation": conversation, "messages": messages,
                           "form": form, "contacts": contacts})


@login_required
def update_message_conversation(request, slug_forum, pk_forum, slug_conversation, pk_conversation, pk_message):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    account = user.retrieve_forum_account(forum)
    conversation = get_object_or_404(Conversation, pk=pk_conversation)
    message = get_object_or_404(Message, pk=pk_message)
    user_permission(message, user)

    if request.method == "POST":
        form = PostMessage(request.POST)
        if form.is_valid():
            message.message = form.cleaned_data["message"]
            message.save()
            return redirect(conversation)
    else:
        form = PostMessage(initial=model_to_dict(message))
    return render(request, "private/update-message.html", context={"forum": forum, "form": form,
                                                                   "conversation": conversation, "account": account})


@require_POST
@login_required
def delete_message_conversation(request, pk_forum, pk_conversation, pk_message):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_active_forum_account(user, forum)
    conversation = get_object_or_404(Conversation, pk=pk_conversation)
    message = get_object_or_404(Message, pk=pk_message)
    user_permission(message, user)
    message.delete()
    return redirect(conversation)


@login_required
def profile_forum(request, pk_forum, slug_forum):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    last_messages = Message.objects.filter(account=account, topic__sub_category__category__forum=forum).order_by(
        "-creation")[:5]

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            account.thumbnail = form.cleaned_data["thumbnail"]
            account.save()
            return redirect(request.path)
    else:
        form = ProfileUpdateForm()
    return render(request, "private/profile.html", context={"forum": forum, "account": account, "form": form,
                                                            "messages": last_messages})
