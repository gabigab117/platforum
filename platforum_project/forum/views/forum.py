from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from forum.models import Forum, Category, ForumAccount, SubCategory, Topic, Message
from forum.forms import CreateTopic


def index(request, slug):
    # Afficher les catégories et sous catégories
    user = request.user
    forum = get_object_or_404(Forum, slug=slug)
    categories = Category.objects.filter(forum=forum)
    return render(request, "forum/index.html", context={"forum": forum, "categories": categories})


def sub_category_view(request, pk, slug_forum, slug_sub_category):
    # Afficher la liste des sujets (pagination)
    # Bouton nouveau sujet
    forum = get_object_or_404(Forum, slug=slug_forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)
    topics = Topic.objects.filter(sub_category=sub_category)
    return render(request, "forum/sub-category.html", context={"sub_category": sub_category,
                                                               "forum": forum,
                                                               "topics": topics})


def add_topic(request, slug_forum, pk, slug_sub_category):
    user = request.user
    forum = get_object_or_404(Forum, slug=slug_forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)

    if request.method == "POST":
        form = CreateTopic(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = user
            topic.sub_category = sub_category
            topic.save()
            Message.objects.create(message=form.cleaned_data["message"], user=user, topic=topic)
            return redirect("landing:index")

    else:
        form = CreateTopic()
    return render(request, "forum/new-topic.html", context={
        "forum": forum,
        "sub_category": sub_category,
        "form": form
    })


def topic_view(request, slug_forum, pk, slug_sub_category, pk_topic, slug_topic):
    user = request.user
    forum = get_object_or_404(Forum, slug=slug_forum)
    sub_category = get_object_or_404(SubCategory, pk=pk)
    topic = get_object_or_404(Topic, pk=pk_topic)
    messages = Message.objects.filter(topic=topic)
    return render(request, "forum/topic.html", context={
        "forum": forum,
        "sub_category": sub_category,
        "topic": topic,
        "messages": messages
    })
