from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from forum.default_data.messages import welcome_message


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    forum = models.ForeignKey(to="Forum", on_delete=models.CASCADE, verbose_name="Forum")
    index = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Catégorie"
        ordering = ["index"]

    def __str__(self):
        return f"{self.name} - {self.forum.name}"

    @classmethod
    def create_test_category(cls, forum):
        return cls.objects.create(name="Catégorie Test", forum=forum)

    @property
    def get_sub_categories(self):
        return SubCategory.objects.filter(category=self)


class SubCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name="Sous catégorie")
    slug = models.SlugField(blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name="Catégorie",
                                 related_name="subcategories")
    index = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.category}"

    @classmethod
    def create_test_subcategory(cls, category):
        return cls.objects.create(name="Sous catégorie Test", category=category)

    @property
    def number_of_messages(self):
        return Message.objects.filter(topic__sub_category=self).count()

    @property
    def last_topic_commented(self):
        try:
            return Message.objects.filter(topic__sub_category=self).last().topic.title
        except AttributeError:
            return "Pas encore de sujet, lance toi ! :)"

    class Meta:
        verbose_name = "Sous catégorie"
        ordering = ["index"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre")
    slug = models.SlugField(blank=True)
    # Système d'alerte si sub_category est null
    sub_category = models.ForeignKey(to=SubCategory, on_delete=models.CASCADE)
    # Si le modérateur souhaite clôturer le sujet sans le supprimer
    closed = models.BooleanField(default=False, verbose_name="Clôturé")
    account = models.ForeignKey(to="ForumAccount", verbose_name="Auteur", on_delete=models.SET_NULL, null=True)
    creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    pin = models.BooleanField(default=False, verbose_name="Epinglé")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="Activité récente")

    class Meta:
        verbose_name = "Sujet"
        ordering = ['-last_activity']

    def __str__(self):
        return f"{self.title} - {self.account.user.username} - {self.sub_category.category.forum}"

    def pin_topic(self):
        self.pin = True
        self.save()
        return self

    def unpin_topic(self):
        self.pin = False
        self.save()
        return self

    @property
    def author(self):
        return self.account.user.username if self.account else "Utilisateur banni"

    @property
    def number_of_messages(self):
        return Message.objects.filter(topic=self).count()

    @property
    def last_message(self):
        return Message.objects.filter(topic=self).last().account.user.username

    @classmethod
    def create_topic_test(cls, sub_category, account):
        return cls.objects.create(title="Bienvenu(e)", sub_category=sub_category, account=account)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        sub_category = self.sub_category
        forum = sub_category.category.forum
        return reverse("forum:topic", kwargs={
            "slug_forum": forum.slug,
            "pk_forum": forum.pk,
            "pk": sub_category.pk,
            "slug_sub_category": sub_category.slug,
            "pk_topic": self.pk,
            "slug_topic": self.slug
        })


class Message(models.Model):
    message = models.TextField(verbose_name="Message")
    account = models.ForeignKey(to="ForumAccount", verbose_name="Auteur", on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(to=Topic, verbose_name="Sujet", on_delete=models.CASCADE, null=True, blank=True)
    conversation = models.ForeignKey(to="Conversation", on_delete=models.CASCADE,
                                     verbose_name="Messagerie Personnel", null=True, blank=True)
    personal = models.BooleanField(verbose_name="Personnel", default=False)
    creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    update = models.DateTimeField(auto_now=True, verbose_name="Modifié le", null=True)
    update_counter = models.IntegerField(default=0, verbose_name="Nombre de maj")

    @property
    def author(self):
        return self.account.user.username if self.account else "Utilisateur banni"

    def __str__(self):
        return f"{self.account.user.username} - {self.creation}"

    @classmethod
    def message_test(cls, topic, account):
        return cls.objects.create(message=welcome_message(account), account=account, topic=topic)

    def save(self, *args, **kwargs):
        if Message.objects.filter(pk=self.pk).exists():
            self.update_counter += 1
        if not Message.objects.filter(pk=self.pk).exists() and not self.personal:
            self.topic.last_activity = timezone.now()
            self.topic.save()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['creation']


class Conversation(models.Model):
    account = models.ForeignKey(to="ForumAccount", on_delete=models.CASCADE, verbose_name="Utilisateur",
                                related_name="messaging")
    contacts = models.ManyToManyField(to="ForumAccount", verbose_name="Contacts")
    forum = models.ForeignKey(to="Forum", on_delete=models.CASCADE, verbose_name="Forum")
    subject = models.CharField(max_length=50, verbose_name="Sujet")
    slug = models.SlugField(blank=True)

    def __str__(self):
        return f"Discussion de {self.account.user.username} - {self.forum}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Conversation"

    @property
    def number_of_messages(self):
        return Message.objects.filter(conversation=self).count()

    @property
    def last_message(self):
        return Message.objects.filter(conversation=self).last().account.user.username

    def get_absolute_url(self):
        return reverse("forum:conversation", kwargs={"slug_forum": self.forum.slug,
                                                     "pk_forum": self.forum.pk,
                                                     "slug_conversation": self.slug,
                                                     "pk_conversation": self.pk})
