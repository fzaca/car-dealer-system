# Generated by Django 5.0.7 on 2024-07-27 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0002_bodytype_alter_car_body_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="is_available",
            field=models.BooleanField(default=True),
        ),
    ]