from django.shortcuts import render, redirect, HttpResponseRedirect

from account.forms import SignUpForm


def signup(request):
    form = SignUpForm()
    return render(request, "account/signup.html", context={"form": form})
