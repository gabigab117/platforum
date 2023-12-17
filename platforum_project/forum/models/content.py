from django.db import models
from .forum import Forum
from forum.default_data.messages import welcome_message
from platforum_project.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    forum = models.ForeignKey(to=Forum, on_delete=models.CASCADE, verbose_name="Forum")

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):
        return f"{self.name} - {self.forum.name}"

    @classmethod
    def create_test_category(cls, forum):
        return cls.objects.create(name="Catégorie Test", forum=forum)


class SubCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name="Sous catégorie")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name="Catégorie",
                                 related_name="subcategories")

    def __str__(self):
        return f"{self.name} - {self.category}"

    @classmethod
    def create_test_subcategory(cls, category):
        return cls.objects.create(name="Sous catégorie Test", category=category)

    @property
    def number_of_messages(self):
        return Message.objects.filter(topic__sub_category=self).count

    class Meta:
        verbose_name = "Sous catégorie"


class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre")
    # Système d'alerte si sub_category est null
    sub_category = models.ForeignKey(to=SubCategory, on_delete=models.CASCADE)
    # Si le modérateur souhaite clôturer le sujet sans le supprimer
    closed = models.BooleanField(default=False, verbose_name="Clôturé")
    user = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name="Auteur", on_delete=models.SET_NULL, null=True)
    creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    pin = models.BooleanField(default=False, verbose_name="Epinglé")

    class Meta:
        verbose_name = "Sujet"
        ordering = ['-creation']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    @property
    def author(self):
        return self.user.username if self.user else "Utilisateur banni"

    @classmethod
    def create_topic_test(cls, sub_category, user):
        return cls.objects.create(title="Bienvenu(e)", sub_category=sub_category, user=user)


class Message(models.Model):
    message = models.CharField(max_length=10000, verbose_name="Message")
    user = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name="Auteur", on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(to=Topic, verbose_name="Sujet", on_delete=models.CASCADE, null=True)
    personal_messaging = models.ForeignKey(to="PersonalMessaging", on_delete=models.CASCADE,
                                           verbose_name="Messagerie Personnel", null=True, blank=True)
    personal = models.BooleanField(verbose_name="Personnel", default=False)
    creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    update = models.DateTimeField(auto_now=True, verbose_name="Modifié le", null=True)

    @property
    def author(self):
        return self.user.username if self.user else "Utilisateur banni"

    def __str__(self):
        return f"{self.user} - {self.creation}"

    @classmethod
    def message_test(cls, topic, user):
        return cls.objects.create(message=welcome_message(user), user=user, topic=topic)

    class Meta:
        ordering = ['-creation']


class PersonalMessaging(models.Model):
    # A gérer avec un get or create
    user_one = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur 1",
                                 related_name="user_one_personal_messaging")
    user_two = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur 2",
                                 related_name="user_two_personal_messaging")

    def __str__(self):
        return f"Discussion entre {self.user_one.username} et {self.user_two.uername}"

    class Meta:
        verbose_name = "Messagerie"
