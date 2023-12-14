from django.core.exceptions import ValidationError
from django.db import models
from .forum import Forum
from platforum_project.settings import AUTH_USER_MODEL


class ForumAccount(models.Model):
    forum = models.ForeignKey(to=Forum, on_delete=models.CASCADE, verbose_name="Forum")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    thumbnail = models.ImageField(upload_to="avatars", verbose_name="Vignette")
    # En cas de modération le modérateur peut désactiver le compte temporairement
    active = models.BooleanField(verbose_name="Actif", default=True)
    joined = models.DateField(verbose_name="Rejoins le", auto_now_add=True)

    def __str__(self):
        return f"{self.forum} - {self.user.username}"

    def clean(self):
        if self.thumbnail.size > 5 * 1024 * 1024:
            raise ValidationError("La taille du fichier ne doit pas dépasser 5MO.")
