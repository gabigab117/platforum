from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from platforum_project.settings import AUTH_USER_MODEL
from django.templatetags.static import static
from django.core.exceptions import ValidationError

from .content import Message


class Forum(models.Model):
    forum_master = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.PROTECT,
                                     verbose_name="Administrateur")
    name = models.CharField(max_length=100, verbose_name="Nom du Forum", unique=True)
    slug = models.SlugField(blank=True)
    theme = models.ForeignKey(to="Theme", verbose_name="Thème", on_delete=models.PROTECT)
    description = models.CharField(max_length=3000, verbose_name="Description")
    creation = models.DateField(auto_now_add=True, verbose_name="Date de création")
    thumbnail = models.ImageField(upload_to="Logo", verbose_name="Logo", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.forum_master.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if self.thumbnail and self.thumbnail.size > 5 * 1024 * 1024:
            raise ValidationError("La taille du fichier ne doit pas dépasser 5MO.")

    def get_absolute_url(self):
        return reverse("forum:index", kwargs={"slug_forum": self.slug, "pk_forum": self.pk})

    @property
    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else static("assets/header.png")


class Theme(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")

    class Meta:
        verbose_name = "Thème"

    def __str__(self):
        return self.name


class ForumAccount(models.Model):
    forum = models.ForeignKey(to=Forum, on_delete=models.CASCADE, verbose_name="Forum")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    thumbnail = models.ImageField(upload_to="avatars", verbose_name="Vignette", null=True, blank=True)
    active = models.BooleanField(verbose_name="Actif", default=True)
    joined = models.DateField(verbose_name="Rejoins le", auto_now_add=True)
    forum_master = models.BooleanField(default=False)
    notification_counter = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.forum} - {self.user.username}"

    def get_absolute_url(self):
        return reverse("forum:member", kwargs={"slug_forum": self.forum.slug,
                                               "pk_forum": self.forum.pk,
                                               "pk_member": self.pk})

    def deactivate(self):
        self.active = False
        self.save()
        return self

    def activate(self):
        self.active = True
        self.save()
        return self

    @property
    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else static("default/default_thumbnail.png")

    @property
    def messages_count(self):
        return Message.objects.filter(account=self).count()

    def clean(self):
        if self.thumbnail and self.thumbnail.size > 5 * 1024 * 1024:
            raise ValidationError("La taille du fichier ne doit pas dépasser 5MO.")

    class Meta:
        verbose_name = "Compte"


class Notification(models.Model):
    account = models.ForeignKey(to="ForumAccount", on_delete=models.CASCADE, verbose_name="Compte")
    message = models.CharField(max_length=200)

    @classmethod
    def notify_member_if_message_posted_in_topic(cls, topic, account):
        if topic.account != account:
            topic.account.notification_counter += 1
            topic.account.save()
            return cls.objects.create(account=topic.account,
                                      message=f"Nouveau message posté par {account.user.username} dans {topic.title}")

    @classmethod
    def notify_member_if_message_posted_in_conversation(cls, conversation, account):
        if conversation.account != account:
            conversation.account.notification_counter += 1
            conversation.account.save()
            return cls.objects.create(account=conversation.account,
                                      message=f"Boite personnelle : Nouveau message posté par {account.user.username} "
                                              f"dans {conversation.subject}")
