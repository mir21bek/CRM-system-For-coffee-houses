from django.contrib import admin

from .models import (
    ClientProfile,
    CustomUser,
    EmployeeProfile,
    EmployeeSchedule,
    EmployeeWorkdays,
)


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = (
        "get_full_name",
        "get_role",
        "get_email",
        "get_date_of_birth",
        "get_phone_number",
    )

    def get_full_name(self, obj):
        return obj.user.full_name

    get_full_name.short_description = "ФИО"

    def get_role(self, obj):
        return obj.user.role

    get_role.short_description = "Позиция"

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Почта"

    def get_date_of_birth(self, obj):
        return obj.user.date_of_birth

    get_date_of_birth.short_description = "Дата рождения"

    def get_phone_number(self, obj):
        return obj.user.phone_number

    get_phone_number.short_description = "Телефон номер"


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "role")


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "get_email")

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Почта"


admin.site.register(EmployeeSchedule)
admin.site.register(EmployeeWorkdays)
