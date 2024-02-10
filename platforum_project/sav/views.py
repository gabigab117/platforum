from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm


def contact_view(request):
    user = request.user

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            text = form.cleaned_data["text"]
            send_mail(subject=subject, message=f"De la part de {email} - {text}",
                      recipient_list=["gabrieltrouve5@gmail.com"], from_email=None)
            send_mail(subject="Email bien envoyé", message="J'ai bien reçu votre email, je réponds rapidement :).",
                      from_email=None, recipient_list=[email])
            messages.add_message(request, messages.INFO,
                                 "Le message a été envoyé, si vous ne recevez pas d'email "
                                 "de confirmation veuillez vérifier vos spams ou renvoyer votre "
                                 "message en vérifiant bien l'email renseigné svp.")
            return redirect("sav:contact")
    else:
        form = ContactForm(initial={"email": user.email}) if user.is_authenticated else ContactForm()

    return render(request, "sav/contact.html", context={"form": form})


def legal_view(request):
    return render(request, "sav/legal.html")
