from django.db import models
from platforum_project.settings import AUTH_USER_MODEL


class Forum(models.Model):
    forum_master = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.PROTECT,
                                     verbose_name="Administrateur")
    name = models.CharField(max_length=100, verbose_name="Nom du Forum")
    description = models.CharField(max_length=1000, verbose_name="Description")
    # Champ field pour le domaine, blabla ou autre
