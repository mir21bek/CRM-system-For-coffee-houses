from django.contrib.auth import password_validation
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, full_name, password, **extra_fields)


def validate_date_of_birth(value):
    if value >= timezone.now().date():
        raise Exception("Date of the birth must be past.")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """This class covers the basic attributes for creating users"""

    ROLE = [
        ("admin", "Admin"),
        ("client", "Client"),
        ("waiter", "Waiter"),
        ("barista", "Barista"),
    ]
    role = models.CharField(
        max_length=20, choices=ROLE, verbose_name="Позиция", null=True
    )
    email = models.EmailField(
        validators=[validate_email],
        verbose_name="почтовый адрес",
        max_length=200,
        unique=True,
    )
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    date_of_birth = models.DateField(
        validators=[validate_date_of_birth],
        verbose_name="Дата рождения",
        blank=True,
        null=True,
    )
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    password = models.CharField(_("password"), max_length=128, blank=True)
    otp = models.PositiveIntegerField(null=True, blank=True, verbose_name="Код")
    otp_expiration = models.DateTimeField(
        null=True, blank=True, verbose_name="Срок кода"
    )
    login = models.CharField(
        max_length=100, unique=True, verbose_name="Логин", null=True, blank=True
    )
    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_users", blank=True
    )
    is_verify = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def __str__(self):
        return f"{self.full_name} {self.email}"

    class Meta:
        verbose_name = "Все пользователи"
        verbose_name_plural = "Мои пользователи"


class ClientProfile(models.Model):
    """This class is for client's profile"""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="client_profile",
        verbose_name="Клиент",
    )
    bonuses = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        verbose_name="Бонусы",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = "Профиль клиента"
        verbose_name_plural = "Профили клиентов"


class EmployeeSchedule(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Загаловка графика (Ночь, День и т.д)"
        verbose_name_plural = "Загаловка графиков (Ночь, День и т.д)"


class EmployeeWorkdays(models.Model):
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
        EmployeeSchedule, on_delete=models.CASCADE, related_name="workdays"
    )
    workday = models.PositiveSmallIntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.schedule.title} - {self.get_workday_display()} - {self.start_time} - {self.end_time}"

    class Meta:
        verbose_name_plural = _("График сотрудников")
        unique_together = [("schedule", "workday")]

    @property
    def duration(self):
        return self.end_time - self.start_time


class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="employee_profile",
        verbose_name="Сотрудник",
    )
    schedule = models.ForeignKey(
        EmployeeSchedule,
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"
