# Generated by Django 4.2.4 on 2023-10-13 19:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_bid_bid_currency_listing_startingbid_currency_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bid",
            name="bid_currency",
        ),
        migrations.RemoveField(
            model_name="listing",
            name="startingBid_currency",
        ),
        migrations.AlterField(
            model_name="bid",
            name="bid",
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name="listing",
            name="startingBid",
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
