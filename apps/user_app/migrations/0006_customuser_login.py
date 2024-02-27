# Generated by Django 5.0.2 on 2024-02-26 19:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_app", "0005_customuser_otp_expiration"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="login",
            field=models.CharField(
                blank=True, max_length=100, null=True, unique=True, verbose_name="Логин"
            ),
        ),
    ]