# Generated by Django 5.0 on 2023-12-26 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0016_remove_personalmessaging_user_one_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalmessaging',
            name='forum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forum', verbose_name='Forum'),
        ),
    ]
