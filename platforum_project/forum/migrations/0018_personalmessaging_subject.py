# Generated by Django 5.0 on 2023-12-26 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0017_alter_personalmessaging_forum'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalmessaging',
            name='subject',
            field=models.CharField(default='', max_length=50, verbose_name='Sujet'),
            preserve_default=False,
        ),
    ]