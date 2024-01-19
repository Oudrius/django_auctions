# Generated by Django 5.0.1 on 2024-01-18 11:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_user_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
