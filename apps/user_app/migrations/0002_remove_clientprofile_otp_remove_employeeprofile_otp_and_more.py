# Generated by Django 5.0.2 on 2024-02-13 15:17

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="clientprofile",
            name="otp",
        ),
        migrations.RemoveField(
            model_name="employeeprofile",
            name="otp",
        ),
        migrations.RemoveField(
            model_name="employeeprofile",
            name="phone_number",
        ),
        migrations.AddField(
            model_name="customuser",
            name="otp",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, null=True, region=None, unique=True
            ),
        ),
    ]
