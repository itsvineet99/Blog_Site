# Generated by Django 5.1.4 on 2024-12-29 05:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="dislike",
            field=models.ManyToManyField(
                related_name="dislike", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="like",
            field=models.ManyToManyField(
                related_name="like", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
