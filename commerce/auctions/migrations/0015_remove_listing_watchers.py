# Generated by Django 4.2.4 on 2023-10-20 18:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0014_alter_user_watching"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="watchers",
        ),
    ]