# Generated by Django 4.2.4 on 2023-10-18 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0007_remove_bid_bid_currency_alter_bid_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="winner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="won_listings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]