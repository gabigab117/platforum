from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from forum.models import Forum, ForumAccount


def index(request):
    return render(request, "landing/index.html")


def forums_list_view(request):
    forums = Forum.objects.all()

    search = request.GET.get("rechercher-forum")
    if search:
        forums = Forum.objects.filter(
            Q(name__icontains=search) | Q(theme__name__icontains=search) | Q(description__icontains=search)
        )
    return render(request, "landing/forums-list.html", context={"forums": forums})


@login_required
def my_forums_list_view(request):
    user = request.user
    myforums = Forum.objects.filter(forum_master=user)
    forums = ForumAccount.objects.filter(user=user)
    return render(request, "landing/myforums.html", context={"myforums": myforums, "forums": forums})


def forum_documentation_view(request):
    return render(request, "documentation/doc.html")


def admin_documentation_view(request):
    return render(request, "documentation/admin.html")
