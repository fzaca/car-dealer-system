# Generated by Django 5.0.7 on 2024-07-19 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_employee"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="is_customer",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_salesperson",
        ),
    ]