# Generated by Django 5.0 on 2023-12-26 19:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_alter_forumaccount_thumbnail'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalmessaging',
            name='user_one',
        ),
        migrations.RemoveField(
            model_name='personalmessaging',
            name='user_two',
        ),
        migrations.AddField(
            model_name='personalmessaging',
            name='contacts',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Contacts'),
        ),
        migrations.AddField(
            model_name='personalmessaging',
            name='forum',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.forum', verbose_name='Forum'),
        ),
        migrations.AddField(
            model_name='personalmessaging',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='messaging', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
            preserve_default=False,
        ),
    ]