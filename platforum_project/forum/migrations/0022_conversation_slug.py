# Generated by Django 5.0 on 2023-12-27 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0021_alter_message_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
