from django.db import models
from .forum import Forum
from platforum_project.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    forum = models.ForeignKey(to=Forum, on_delete=models.CASCADE, verbose_name="Forum")


class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre")
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True)
    # Si le modérateur souhaite clôturer le sujet sans le supprimer
    closed = models.BooleanField(default=False, verbose_name="Clôturé")
    user = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name="Auteur", on_delete=models.SET_NULL, null=True)

    @property
    def author(self):
        return self.user.username if self.user else "Utilisateur banni"


class Message(models.Model):
    message = models.CharField(max_length=10000, verbose_name="Message")
    user = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name="Auteur", on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(to=Topic, verbose_name="Sujet", on_delete=models.CASCADE, null=True)
    personal_messaging = models.ForeignKey(to="PersonalMessaging", on_delete=models.CASCADE,
                                           verbose_name="Messagerie Personnel", null=True)
    personal = models.BooleanField(verbose_name="Personnel", default=False)

    @property
    def author(self):
        return self.user.username if self.user else "Utilisateur banni"


class PersonalMessaging(models.Model):
    user_one = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur 1",
                                 related_name="user_one_personal_messaging")
    user_two = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur 2",
                                 related_name="user_two_personal_messaging")

    def __str__(self):
        return f"Discussion entre {self.user_one.username} et {self.user_two.uername}"
