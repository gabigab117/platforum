from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect

from platforum_project.func.security import user_permission, active_forum_account
from forum.models import Forum, Category, ForumAccount, SubCategory, Topic, Message
from forum.forms import CreateTopic, PostMessage


def index(request, slug_forum, pk_forum):
    # Afficher les catégories et sous catégories
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    categories = Category.objects.filter(forum=forum)
    return render(request, "forum/index.html", context={"forum": forum, "categories": categories})


def sub_category_view(request, pk, slug_forum, pk_forum, slug_sub_category):
    # Afficher la liste des sujets (pagination)
    # Bouton nouveau sujet
    forum = get_object_or_404(Forum, pk=pk_forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)
    topics = Topic.objects.filter(sub_category=sub_category, pin=False)
    pin_topics = Topic.objects.filter(sub_category=sub_category, pin=True)
    return render(request, "forum/sub-category.html", context={"sub_category": sub_category,
                                                               "forum": forum,
                                                               "topics": topics, "pin_topics": pin_topics})


@login_required
def add_topic(request, slug_forum, pk_forum, pk, slug_sub_category):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = active_forum_account(user, forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)

    if request.method == "POST":
        form = CreateTopic(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = user
            topic.sub_category = sub_category
            topic.save()
            Message.objects.create(message=form.cleaned_data["message"], user=user, topic=topic)
            return redirect(topic)

    else:
        form = CreateTopic()
    return render(request, "forum/new-topic.html", context={
        "forum": forum,
        "sub_category": sub_category,
        "form": form
    })


def topic_view(request, slug_forum, pk_forum, pk, slug_sub_category, pk_topic, slug_topic):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)
    topic = get_object_or_404(Topic, pk=pk_topic)
    messages = Message.objects.filter(topic=topic)
    account = active_forum_account(user, forum)

    if request.method == "POST":
        form = PostMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.topic = topic
            message.user = user
            message.save()
            return redirect(topic)
    else:
        form = PostMessage()
    return render(request, "forum/topic.html", context={
        "forum": forum,
        "sub_category": sub_category,
        "topic": topic,
        "messages": messages,
        "account": account,
        "form": form
    })


@login_required
def update_message(request, slug_forum, pk_forum, pk, slug_sub_category, pk_topic, slug_topic, pk_message):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)
    topic = get_object_or_404(Topic, pk=pk_topic)
    account = active_forum_account(user, forum)
    message = get_object_or_404(Message, pk=pk_message)
    user_permission(message, user)

    if request.method == "POST":
        form = PostMessage(request.POST)
        if form.is_valid():
            message.message = form.cleaned_data["message"]
            message.save()
            return redirect(topic)
    else:
        form = PostMessage(initial=model_to_dict(message))
    return render(request, "forum/update-message.html", context={
        "forum": forum,
        "topic": topic,
        "message": message,
        "form": form,
        "sub_category": sub_category
    })


@login_required
@require_POST
def delete_message(request, pk_forum, pk_topic, pk_message):
    user = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = active_forum_account(user, forum)
    message = get_object_or_404(Message, pk=pk_message)
    user_permission(message, user)
    message.delete()
    return redirect(Topic.objects.get(pk=pk_topic))
