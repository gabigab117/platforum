from django.shortcuts import render
from .forms import CreateForumForm


def create_forum(request):
    # Créer en cascade en une fois : Forum, AccountForum de l'admin, Categorie Test, Sujet Test
    form = CreateForumForm()
    return render(request, "forum/create-forum.html", context={"form": form})
