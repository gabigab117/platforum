# Generated by Django 5.0 on 2023-12-26 21:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0018_personalmessaging_subject'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PersonalMessaging',
            new_name='Conversation',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='personal_messaging',
            new_name='conversation',
        ),
    ]
