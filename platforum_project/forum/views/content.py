from django.db import models
from .forum import Forum
from platforum_project.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    forum = models.ForeignKey(to=Forum, on_delete=models.CASCADE, verbose_name="Forum")


class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre")
    category = models.ForeignKey(to=Category, on_delete=models.SET_DEFAULT)
    # Si le modérateur souhaite clôturer le sujet sans le supprimer
    closed = models.BooleanField(default=False, verbose_name="Clôturé")
    user = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name="Auteur", on_delete=models.SET_NULL, null=True)

    @property
    def author(self):
        return self.user.username if self.user else "Utilisateur banni"


class Message(models.Model):
    message = models.CharField(max_length=10000, verbose_name="Message")
    # Penser à créer une propriété (return user.username if user else "User banni")
    user = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name="Auteur", on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(to=Topic, verbose_name="Sujet", on_delete=models.CASCADE)

    @property
    def author(self):
        return self.user.username if self.user else "Utilisateur banni"
