# Generated by Django 5.0.6 on 2024-08-03 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0014_rename_profile_photo_inventory_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="inventory",
            name="unit_of_measure",
        ),
    ]
