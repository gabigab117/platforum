# Generated by Django 5.0 on 2023-12-20 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_alter_forum_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['creation']},
        ),
        migrations.AddField(
            model_name='message',
            name='update_counter',
            field=models.IntegerField(default=0, verbose_name='Nombre de maj'),
        ),
    ]