# Generated by Django 5.0.1 on 2024-01-05 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumaccount',
            name='forum_master',
            field=models.BooleanField(default=False),
        ),
    ]