# Generated by Django 5.0 on 2024-01-02 15:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("suppliers", "0002_supplylog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supplier",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="supplier",
            name="modified",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="supplylog",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="supplylog",
            name="modified",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
