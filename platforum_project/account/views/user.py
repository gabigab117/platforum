from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from account.forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing:index")
        # Penser à revenir pour ajouter un message de confirmation
    else:
        form = SignUpForm()
    return render(request, "account/signup.html", context={"form": form})


class LoginUser(LoginView):
    template_name = "account/login.html"
    next_page = reverse_lazy("landing:index")


def logout_view(request):
    logout(request)
    return redirect("landing:index")
