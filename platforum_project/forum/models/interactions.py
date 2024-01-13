from django.db import models


class Notification(models.Model):
    account = models.ForeignKey(to="ForumAccount", on_delete=models.CASCADE, verbose_name="Compte")
    message = models.CharField(max_length=200)

    @classmethod
    def notify_member_if_message_posted_in_topic(cls, topic, account):
        if topic.account != account:
            topic.account.notification_counter += 1
            topic.account.save(update_fields=["notification_counter"])
            return cls.objects.create(account=topic.account,
                                      message=f"Nouveau message posté par {account.user.username} dans {topic.title}")

    @classmethod
    def notify_member_if_message_posted_in_conversation(cls, conversation, account):
        if conversation.account != account:
            conversation.account.notification_counter += 1
            conversation.account.save(update_fields=["notification_counter"])
            return cls.objects.create(account=conversation.account,
                                      message=f"Boite personnelle : Nouveau message posté par {account.user.username} "
                                              f"dans {conversation.subject}")


class Like(models.Model):
    message = models.ForeignKey(to="Message", on_delete=models.CASCADE)
    liker = models.ForeignKey(to="ForumAccount", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.liker} - {self.message}"

    @classmethod
    def like_unlike(cls, liker, message):
        like, created = cls.objects.get_or_create(message=message, liker=liker)
        if not created:
            like.delete()
