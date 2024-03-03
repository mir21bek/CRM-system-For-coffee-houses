from django.contrib import admin
from .models import BranchSchedule, BranchWorkdays, Branches


@admin.register(Branches)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("branch_name", "slug", "address", "phone_number", "table_quantity")
    prepopulated_fields = {"slug": ("branch_name",)}


@admin.register(BranchSchedule)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(BranchWorkdays)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("schedule", "workday", "start_time", "end_time")
