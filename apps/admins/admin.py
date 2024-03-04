from django.contrib import admin
from .models import (
    BranchSchedule,
    BranchWorkdays,
    Branches,
    Product,
    Menu,
    Category,
    ExtraProduct,
    Recipe,
)


@admin.register(Branches)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("branch_name", "slug", "address", "phone_number", "table_quantity")
    prepopulated_fields = {"slug": ("branch_name",)}


@admin.register(BranchSchedule)
class BranchScheduleAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(BranchWorkdays)
class BranchWorkdaysAdmin(admin.ModelAdmin):
    list_display = ("schedule", "workday", "start_time", "end_time")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "quantity",
        "limit",
        "arrival_date",
        "product_category",
    )


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name_dish", "category", "price")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "description")


@admin.register(ExtraProduct)
class ExtraProductAdmin(admin.ModelAdmin):
    list_display = ("product", "extra_product_quantity")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("menu", "quantity", "choice_unit")
