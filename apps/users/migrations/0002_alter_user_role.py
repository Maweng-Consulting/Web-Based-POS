# Generated by Django 5.0 on 2023-12-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("cashier", "Cashier"),
                    ("agent", "Agent"),
                    ("broker", "Broker"),
                ],
                max_length=32,
                null=True,
            ),
        ),
    ]
