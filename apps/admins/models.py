from django.db import models
from django.utils.translation import gettext_lazy as _


class BranchSchedule(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Загаловка графика"
        verbose_name_plural = "Загаловка графиков"


class BranchWorkdays(models.Model):
    WEEKDAYS = [
        (1, _("Monday")),
        (2, _("Tuesday")),
        (3, _("Wednesday")),
        (4, _("Thursday")),
        (5, _("Friday")),
        (6, _("Saturday")),
        (7, _("Sunday")),
    ]

    schedule = models.ForeignKey(
        BranchSchedule, on_delete=models.CASCADE, related_name="workdays"
    )
    workday = models.PositiveSmallIntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.schedule.title} - {self.get_workday_display()} - {self.start_time} - {self.end_time}"

    class Meta:
        verbose_name_plural = _("График филиала")
        unique_together = [("schedule", "workday")]

    @property
    def duration(self):
        return self.end_time - self.start_time


class Branches(models.Model):
    branch_name = models.CharField(max_length=200, verbose_name="Название филиала")
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone_number = models.CharField(max_length=17, verbose_name="Тел. номер")
    link_on_2gis = models.URLField(
        max_length=255, verbose_name="Ссылка на 2Gis", null=True, blank=True
    )
    image1 = models.ImageField(verbose_name="Фото заведения", blank=True, null=True)
    image2 = models.ImageField(verbose_name="Фото заведения", blank=True, null=True)
    image3 = models.ImageField(verbose_name="Фото заведения", blank=True, null=True)
    image4 = models.ImageField(verbose_name="Фото заведения", blank=True, null=True)
    table_quantity = models.PositiveIntegerField(
        verbose_name="Количество столов", db_index=True, null=True
    )
    schedule = models.ManyToManyField(
        BranchWorkdays,
        related_name="branch_schedule",
        blank=True,
    )

    class Meta:
        indexes = [models.Index(fields=["branch_name"])]
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    def __str__(self):
        return self.branch_name
