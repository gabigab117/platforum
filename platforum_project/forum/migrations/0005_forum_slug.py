# Generated by Django 5.0 on 2023-12-14 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_alter_subcategory_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
