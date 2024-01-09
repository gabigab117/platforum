from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from account.forms import SignUpForm
from forum.models import ForumAccount, Message, Topic


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, level=messages.INFO,
                                 message="Vous êtes désormais inscrit."
                                         "Vous pouvez désormais adhérer à des forums ou créer le votre !")
            return redirect("landing:index")
    else:
        form = SignUpForm()
    return render(request, "account/signup.html", context={"form": form})


class LoginUser(LoginView):
    template_name = "account/login.html"
    next_page = reverse_lazy("landing:index")


@login_required
def logout_view(request):
    logout(request)
    return redirect("landing:index")


@login_required
def profile_view(request):
    user = request.user
    forum_accounts = ForumAccount.objects.filter(user=user).count()
    messages = Message.objects.filter(account__user=user).count()
    topics = Topic.objects.filter(account__user=user).count()
    return render(request, "account/profile.html", context={"forum_accounts": forum_accounts,
                                                            "messages": messages, "topics": topics})
