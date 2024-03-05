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
    branch_name = models.CharField(
        max_length=200, verbose_name="Название филиала", db_index=True
    )
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
    menu = models.ForeignKey(
        "admins.Menu",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Меню",
        related_name="branch_menu",
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


class Product(models.Model):
    MEASURER_UNIT_CHOICES = [
        ("kg", "кг."),
        ("g", "гр."),
        ("l", "лит."),
        ("ml", "мл."),
        ("unit", "шт"),
    ]
    PRODUCT_CATEGORY = [
        ("ready_products", "Готовые продукты"),
        ("raw_materials", "Сырье"),
    ]
    product_name = models.CharField(max_length=150, verbose_name="Наименование")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    limit = models.PositiveIntegerField(default=0, verbose_name="Лимит")
    arrival_date = models.DateField(verbose_name="Дата прихода")
    branch = models.ManyToManyField(
        Branches, verbose_name="Филилалы", related_name="branch_in_product"
    )
    unit_quantity = models.CharField(
        max_length=20,
        choices=MEASURER_UNIT_CHOICES,
        verbose_name="Единица измерения (Количество)",
    )
    product_category = models.CharField(
        max_length=20, choices=PRODUCT_CATEGORY, verbose_name="Категория продукта"
    )
    is_running_out = models.BooleanField(
        default=False, verbose_name="Заканчивающийся продукт"
    )

    class Meta:
        ordering = ["-arrival_date", "product_name"]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.product_name


class Category(models.Model):
    category_name = models.CharField(
        max_length=50, verbose_name="Категория", db_index=True
    )
    description = models.CharField(
        max_length=500, verbose_name="Описание", null=True, blank=True
    )
    image = models.ImageField(verbose_name="Фото категории", null=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.category_name


class ExtraProduct(models.Model):
    MEASURER_UNIT_CHOICES = [
        ("kg", "кг."),
        ("g", "гр."),
        ("l", "лит."),
        ("ml", "мл."),
        ("unit", "шт"),
    ]
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        related_name="extra_product",
    )
    quantity = models.IntegerField(verbose_name="Количество", null=True)
    extra_product_quantity = models.CharField(
        max_length=20, choices=MEASURER_UNIT_CHOICES, verbose_name="Измерения"
    )

    class Meta:
        verbose_name = "Доп. продукт"
        verbose_name_plural = "Доп. продукты"

    def __str__(self):
        return f"Наименование: {self.product.product_name}"


class Menu(models.Model):
    name_dish = models.CharField(
        max_length=200, verbose_name="Наименование", db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="menu_category",
    )
    products = models.ManyToManyField(
        Product,
        through="Recipe",
        verbose_name="Состав блюда и граммовка",
    )
    price = models.DecimalField(
        decimal_places=2, max_digits=5, verbose_name="Стоимость"
    )

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.name_dish


class Recipe(models.Model):
    MEASURER_UNIT_CHOICES = [
        ("kg", "кг."),
        ("g", "гр."),
        ("l", "лит."),
        ("ml", "мл."),
        ("unit", "шт"),
    ]
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    choice_unit = models.CharField(max_length=20, choices=MEASURER_UNIT_CHOICES)

    class Meta:
        verbose_name = "Тех. карта"
        verbose_name_plural = "Тех. карта"

    def __str__(self):
        return f"Наименование: {self.menu.name_dish}"
