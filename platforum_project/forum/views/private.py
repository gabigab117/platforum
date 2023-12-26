from django.shortcuts import render, redirect, get_object_or_404

from forum.models import Conversation, Forum


def personal_messaging(request, slug_forum):
    user = request.user
    forum = get_object_or_404(Forum, slug=slug_forum)
    conversations = Conversation.objects.filter(forum=forum, user=user)
    return render(request, "private/personal-messaging.html", context={
        "forum": forum,
        "conversations": conversations
    })
