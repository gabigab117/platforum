from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from forum.forms import CreateForumForm
from forum.default_data.default_forum_data import create_forum_with_data


@login_required
def create_forum(request):
    user = request.user
    if request.method == "POST":
        form = CreateForumForm(request.POST)
        if form.is_valid():
            forum = create_forum_with_data(form, user)
            return redirect("forum:index", slug_forum=forum.slug, pk_forum=forum.pk)

    form = CreateForumForm()
    return render(request, "creation/create-forum.html", context={"form": form})
