# Generated by Django 5.0.1 on 2024-01-17 11:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_category_listing_created_by_listing_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
            preserve_default=False,
        ),
    ]
