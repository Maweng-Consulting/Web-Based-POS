# Generated by Django 5.0 on 2023-12-29 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0001_initial"),
        ("suppliers", "0002_supplylog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supplyinvoice",
            name="supplier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supplierinvoices",
                to="suppliers.supplier",
            ),
        ),
    ]
