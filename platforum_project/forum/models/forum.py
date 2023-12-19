from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from platforum_project.settings import AUTH_USER_MODEL


class Forum(models.Model):
    forum_master = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.PROTECT,
                                     verbose_name="Administrateur")
    name = models.CharField(max_length=100, verbose_name="Nom du Forum")
    slug = models.SlugField(blank=True)
    theme = models.ForeignKey(to="Theme", verbose_name="Thème", on_delete=models.PROTECT)
    description = models.CharField(max_length=1000, verbose_name="Description")
    creation = models.DateField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return f"{self.name} - {self.forum_master.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("forum:index", kwargs={"slug": self.slug})


class Theme(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")

    class Meta:
        verbose_name = "Thème"

    def __str__(self):
        return self.name
