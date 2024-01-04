from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from forum.models import ForumAccount


class CustomManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password, **kwargs):
        if not username:
            raise ValueError("Username must be set")
        if not email:
            raise ValueError("Email must be set")
        if not first_name:
            raise ValueError("First name must be set")
        if not last_name:
            raise ValueError("Last name must be set")

        user = self.model(username=username, email=self.normalize_email(email), first_name=first_name,
                          last_name=last_name, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, first_name, last_name, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, email, first_name, last_name, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # With REQUIRED_FIELDS : If the field is empty at the time of creation: "This field cannot be empty"
    REQUIRED_FIELDS = ["email", "last_name", "first_name"]
    objects = CustomManager()

    def retrieve_forum_account(self, forum):
        try:
            return ForumAccount.objects.get(user=self, forum=forum)
        except ObjectDoesNotExist:
            return None
