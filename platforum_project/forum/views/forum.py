from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from forum.models import Forum, Category, ForumAccount, SubCategory, Topic, Message


@login_required
def index(request, slug):
    # Afficher les catégories et sous catégories
    user = request.user
    forum = get_object_or_404(Forum, slug=slug)
    categories = Category.objects.filter(forum=forum)
    return render(request, "forum/index.html", context={"forum": forum, "categories": categories})
