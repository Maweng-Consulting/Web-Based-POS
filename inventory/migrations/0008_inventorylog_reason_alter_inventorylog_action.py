# Generated by Django 5.0 on 2023-12-29 12:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0007_alter_inventorylog_item"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventorylog",
            name="reason",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="inventorylog",
            name="action",
            field=models.CharField(
                choices=[
                    ("Buy", "Buy"),
                    ("Sale", "Sale"),
                    ("Damaged", "Damaged"),
                    ("Stolen", "Stolen"),
                    ("Family", "Family use"),
                    ("Fashion", "Out of fashion"),
                    ("New Stock", "New Stock"),
                    ("Stock Edit", "Stock Edited"),
                    ("Stock Delete", "Stock Delete"),
                ],
                max_length=255,
            ),
        ),
    ]
