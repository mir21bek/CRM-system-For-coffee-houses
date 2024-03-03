# Generated by Django 5.0.2 on 2024-02-21 19:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "user_app",
            "0003_alter_clientprofile_options_alter_customuser_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                max_length=200,
                unique=True,
                validators=[django.core.validators.EmailValidator()],
                verbose_name="почтовый адрес",
            ),
        ),
    ]
