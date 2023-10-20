# Generated by Django 4.2.4 on 2023-10-19 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0008_listing_winner"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bid",
            old_name="listing_id",
            new_name="listing",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="listing_id",
            new_name="listing",
        ),
        migrations.AlterField(
            model_name="listing",
            name="category",
            field=models.CharField(
                choices=[
                    ("auto", "Auto"),
                    ("clothing", "Clothing"),
                    ("electronics", "Electronics"),
                    ("home", "Home"),
                    ("jewelry", "Jewelry"),
                    ("sportingGoods", "Sporting Goods"),
                    ("toys", "Toys"),
                ],
                max_length=32,
            ),
        ),
    ]
