# PlatForum

## Introduction

PlatForum is a forum builder. With this project, a user can create an account and then be able to
create their own forum(s), and build their categories and subcategories as they wish.

Also, a user can come to PlatForum to participate in one or more forums as a "member," without necessarily
being the creator.

**What happens at the account level?**

A user account is required to access Platforum, and then when a user wants to join a forum, or create their own,
an account per forum will be created. This can be seen as "sub-accounts" that are attached to the user account of the
platform.

## Prerequisites

### requirments.txt

```
asgiref==3.7.2
crispy-bootstrap5==2023.10
Django==5.0.1
django-ckeditor==6.7.0
django-crispy-forms==2.1
django-environ==0.11.2
django-js-asset==2.2.0
django-recaptcha==4.0.0
iniconfig==2.0.0
packaging==23.2
pillow==10.2.0
pluggy==1.3.0
pytest==7.4.4
pytest-django==4.7.0
pytest-mock==3.12.0
sqlparse==0.4.4
```

### settings.py

I added constants in my settings file to manage Crispy Forms, reCAPTCHA, the mail server, and CKEditor.

But you need to add your site to Google reCAPTCHA: https://www.google.com/recaptcha/admin/create,
choose reCAPTCHA v2 and add the domain 127.0.0.1 for it to work locally.

**For reCAPTCHA, I am using the test keys:**

```
# Recaptcha
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
```

**For the emails :**

You need a Google application email address and password. Or you can modify my constants to
adapt to the mail server you want to use.

```
# Emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'gabrieltrouve5@gmail.com'
EMAIL_HOST_PASSWORD = env('EMAIL_PW')
DEFAULT_FROM_EMAIL = 'PlatForum<gabrieltrouve5@gmail.com>'
```

Fichier ```.env``` que je gère avec django-environ.

## Account App

I created a CustomUser model. When signing up, users must activate their account by clicking on a link received by
email.

I created (using Django's tools) an account activation system myself. I did not use a library for
this as I wanted something lightweight. See the ```verification``` package in the ```account``` application.

After activating their accounts, users can start to create or join forums.

They can also change their password or request a new one via email.

## Landing App

The landing application is used for the index page of the platform and also for the menu that allows access to
the creation of a forum, displaying the list of forums, and the documentation.

A search engine is included to search for a forum.

*Forum Search Engine :*

```
search = request.GET.get("rechercher-forum")
    if search:
        forums = Forum.objects.filter(
            Q(name__icontains=search) | Q(theme__name__icontains=search) | Q(description__icontains=search)
        )
```

## SAV app

The SAV (Customer Service) application is used to manage the contact form. I created a standalone application because
the
SAV system could evolve...

## Forum app (The heart of the project! :) )

### Models

**Forum**: The Forum model.

**Theme**: Forums are associated with themes.

**ForumAccount**: An account per Forum, linked to the CustomUserModel.

**Badge**: A user (ForumAccount) will be awarded badges based on their participation.

**Category**: In a forum, there are categories.

**SubCategory**: In a category, there are sub-categories.

**Topic**: In a sub-category, there are discussions.

**Message**: In a discussion, there are messages. But a message can exist outside a discussion, as part of
a private messaging system (conversation).

**Conversation**: This is the private version of the Topic model.

**Notification**: Used to create notifications for each ForumAccount.

**Like**: Allows creating a Like instance for each message and user who likes it.

## Views

The creator of the Forum has access to an admin area where they can manage members, have an overview, and create
categories and subcategories.

In its general functioning, the forum allows for the creation of discussions, posting messages, having a
private messaging system, and viewing one's profile (per forum).
The forum creator can edit or delete topics and messages. A user can only edit or
delete their own messages.

*Instance Forum Search Engine :*

```
search = request.GET.get("query")
    if search:
        topics = Topic.objects.filter(title__icontains=search)
        messages = Message.objects.filter(
            Q(personal=False),
            Q(message__icontains=search) | Q(topic__title__icontains=search)
        )
```
