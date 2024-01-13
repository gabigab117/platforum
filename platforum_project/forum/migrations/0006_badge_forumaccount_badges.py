# Generated by Django 5.0.1 on 2024-01-13 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_forumaccount_notification_counter_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('thumbnail', models.ImageField(upload_to='badges', verbose_name='Image')),
            ],
        ),
        migrations.AddField(
            model_name='forumaccount',
            name='badges',
            field=models.ManyToManyField(blank=True, to='forum.badge'),
        ),
    ]