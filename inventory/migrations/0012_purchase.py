# Generated by Django 5.0 on 2024-01-14 22:23

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0011_alter_inventory_created_alter_inventory_modified_and_more"),
        ("suppliers", "0005_alter_supplier_created_alter_supplier_modified_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Purchase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "cost",
                    models.DecimalField(decimal_places=2, default=0, max_digits=100),
                ),
                (
                    "amount_paid",
                    models.DecimalField(decimal_places=2, default=0, max_digits=100),
                ),
                (
                    "purchase_type",
                    models.CharField(
                        choices=[("Paid", "Paid"), ("Credit", "Credit")],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "recorded_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="suppliers.supplier",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
