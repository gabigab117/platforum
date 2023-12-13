from django.db import models
from .forum import Forum
from platforum_project.settings import AUTH_USER_MODEL


class ForumAccount(models.Model):
    forum = models.ForeignKey(to=Forum, on_delete=models.CASCADE, verbose_name="Forum")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    # En cas de modération le modérateur peut désactiver le compte temporairement
    active = models.BooleanField(verbose_name="Actif", default=True)
    joined = models.DateField(verbose_name="Rejoins le", auto_now_add=True)
