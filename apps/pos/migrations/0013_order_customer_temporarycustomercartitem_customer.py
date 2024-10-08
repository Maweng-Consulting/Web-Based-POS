# Generated by Django 5.0 on 2024-01-15 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pos", "0012_alter_creditorder_created_alter_creditorder_modified_and_more"),
        ("users", "0007_alter_customer_created_alter_customer_modified_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.customer",
            ),
        ),
        migrations.AddField(
            model_name="temporarycustomercartitem",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.customer",
            ),
        ),
    ]
