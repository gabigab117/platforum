from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CreateForumForm


@login_required
def create_forum(request):
    # Créer en cascade en une fois : Forum, AccountForum de l'admin, Categorie Test, Sujet Test
    form = CreateForumForm()
    return render(request, "forum/create-forum.html", context={"form": form})
