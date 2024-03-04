# Generated by Django 5.0.2 on 2024-03-03 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BranchSchedule",
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
                ("title", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Загаловка графика",
                "verbose_name_plural": "Загаловка графиков",
            },
        ),
        migrations.CreateModel(
            name="BranchWorkdays",
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
                (
                    "workday",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Monday"),
                            (2, "Tuesday"),
                            (3, "Wednesday"),
                            (4, "Thursday"),
                            (5, "Friday"),
                            (6, "Saturday"),
                            (7, "Sunday"),
                        ]
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workdays",
                        to="admins.branchschedule",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "График сотрудников",
                "unique_together": {("schedule", "workday")},
            },
        ),
        migrations.CreateModel(
            name="Branches",
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
                (
                    "branch_name",
                    models.CharField(max_length=200, verbose_name="Название филиала"),
                ),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("address", models.CharField(max_length=255, verbose_name="Адрес")),
                (
                    "phone_number",
                    models.CharField(max_length=17, verbose_name="Тел. номер"),
                ),
                (
                    "link_on_2gis",
                    models.CharField(max_length=255, verbose_name="Ссылка на 2Gis"),
                ),
                (
                    "image1",
                    models.ImageField(upload_to="", verbose_name="Фото заведения"),
                ),
                (
                    "image2",
                    models.ImageField(upload_to="", verbose_name="Фото заведения"),
                ),
                (
                    "image3",
                    models.ImageField(upload_to="", verbose_name="Фото заведения"),
                ),
                (
                    "image4",
                    models.ImageField(upload_to="", verbose_name="Фото заведения"),
                ),
                (
                    "table_quantity",
                    models.PositiveIntegerField(
                        db_index=True, verbose_name="Количество столов"
                    ),
                ),
                (
                    "schedule",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employees",
                        to="admins.branchworkdays",
                    ),
                ),
            ],
        ),
    ]