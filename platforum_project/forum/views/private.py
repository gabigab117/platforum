from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404

from forum.models import Conversation, Forum, ForumAccount, Message
from forum.forms import PostMessage

from platforum_project.func.security import user_permission


def personal_messaging(request, slug_forum):
    user = request.user
    forum = get_object_or_404(Forum, slug=slug_forum)
    my_conversations = Conversation.objects.filter(forum=forum, user=user)
    conversations = Conversation.objects.filter(forum=forum, contacts=user)
    return render(request, "private/personal-messaging.html", context={
        "forum": forum,
        "my_conversations": my_conversations, "conversations": conversations
    })


def conversation_view(request, slug_forum, slug_conversation, pk_conversation):
    user = request.user
    forum = get_object_or_404(Forum, slug=slug_forum)
    conversation = get_object_or_404(Conversation, pk=pk_conversation)
    account = ForumAccount(forum=forum, user=user)
    messages = Message.objects.filter(conversation=conversation)
    contacts = conversation.contacts.all()

    if user != conversation.user and user not in contacts:
        raise PermissionDenied()

    if request.method == "POST":
        form = PostMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation, message.user = conversation, user
            message.save()
            return redirect(conversation)
    else:
        form = PostMessage()
    return render(request, "private/conversation.html",
                  context={"account": account, "forum": forum, "conversation": conversation, "messages": messages,
                           "form": form, "contacts": contacts})


def update_message_conversation(request, slug_forum, slug_conversation, pk_conversation, pk_message):
    user = request.user
    forum = get_object_or_404(Forum, slug=slug_forum)
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
                                                                   "conversation": conversation})
