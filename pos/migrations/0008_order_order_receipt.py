# Generated by Django 5.0 on 2024-01-02 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pos", "0007_alter_order_created_alter_order_modified_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_receipt",
            field=models.FileField(null=True, upload_to="receipts/"),
        ),
    ]
