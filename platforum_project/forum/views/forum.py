from django.shortcuts import render


def index(request, slug):
    return render(request, "forum/index.html")
