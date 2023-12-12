from django.db import models
from platforum_project.settings import AUTH_USER_MODEL
from forum.func.default_value import DEFAULT_ADMIN


class Forum(models.Model):
    forum_master = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=DEFAULT_ADMIN,
                                     verbose_name="Administrateur")
    name = models.CharField(max_length=100, verbose_name="Nom du Forum")
