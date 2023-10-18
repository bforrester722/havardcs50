# Generated by Django 4.2.4 on 2023-10-13 20:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_bid_bid_currency_alter_bid_bid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bid",
            name="bid_currency",
        ),
        migrations.AlterField(
            model_name="bid",
            name="bid",
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
