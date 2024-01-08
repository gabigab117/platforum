from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from forum.models import Forum


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
    forums = Forum.objects.filter(forum_master=request.user)
    return render(request, "landing/myforums.html", context={"forums": forums})
