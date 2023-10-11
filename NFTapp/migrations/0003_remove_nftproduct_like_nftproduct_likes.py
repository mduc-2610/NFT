# Generated by Django 4.2.5 on 2023-10-11 13:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NFTapp', '0002_alter_user_cover_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nftproduct',
            name='like',
        ),
        migrations.AddField(
            model_name='nftproduct',
            name='likes',
            field=models.ManyToManyField(default=0, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
