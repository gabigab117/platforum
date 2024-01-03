# Generated by Django 5.0 on 2023-12-28 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0022_conversation_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['-last_activity'], 'verbose_name': 'Sujet'},
        ),
        migrations.AddField(
            model_name='topic',
            name='last_activity',
            field=models.DateTimeField(auto_now=True, verbose_name='Activité récente'),
        ),
    ]