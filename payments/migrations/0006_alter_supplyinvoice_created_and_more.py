# Generated by Django 5.0 on 2024-01-02 15:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0005_alter_supplyinvoice_status_supplyinvoicelog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supplyinvoice",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="supplyinvoice",
            name="modified",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="supplyinvoicelog",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="supplyinvoicelog",
            name="modified",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
