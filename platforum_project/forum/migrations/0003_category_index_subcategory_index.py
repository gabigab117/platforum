# Generated by Django 5.0.1 on 2024-01-07 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_forumaccount_forum_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='index',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]
