from smtplib import SMTPAuthenticationError

from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from account.forms import SignUpForm
from account.verification import send_email_verification, email_verification_token
from forum.models import ForumAccount, Message, Topic


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            try:
                send_email_verification(request, user)
                messages.add_message(request, level=messages.INFO,
                                     message="Vous êtes désormais inscrit."
                                             "Merci d'activer votre compte avec le lien reçu par email, "
                                             "si vous ne l'avez pas reçu, merci de nous contacter.")
            except SMTPAuthenticationError:
                messages.add_message(request, level=messages.INFO,
                                     message="Une erreur est survenue avec l'envoi de l'email. Merci de nous contacter"
                                             "via l'onglet contact en précisant votre adresse email et"
                                             " votre nom de connexion pour que l'on puisse activer votre compte.")
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


def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, "Votre compte est désormait actif, vous pouvez vous connecter")
        return redirect("landing:index")
    else:
        messages.add_message(request, messages.INFO,
                             "Vous pouvez nous contacter par email, nous résoudrons le problème")
        return redirect("landing:index")
