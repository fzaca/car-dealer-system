# Generated by Django 5.0.7 on 2024-07-27 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0002_paymentmethod_invoice_payment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="invoice",
            old_name="pdf",
            new_name="pdf_url",
        ),
    ]