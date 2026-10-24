from django.db import models
from django.conf import settings
from decimal import Decimal

from pathlib import Path
from .image_utils import process_image


class Product(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if self.image and not self.image._committed:
            original_name = Path(self.image.name).stem

            original, thumbnail = process_image(self.image)

            self.image.save(
                f"{original_name}.jpg",
                original,
                save=False,
            )
            self.thumbnail.save(
                f"{original_name}_thumb.jpg",
                thumbnail,
                save=False,
            )

        super().save(*args, **kwargs)

    name = models.CharField(
        verbose_name="Название",
        max_length=100,
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    image = models.ImageField(
        upload_to="product/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    thumbnail = models.ImageField(
        upload_to="products/thumbnails/",
        blank=True,
        null=True,
        editable=False,
        verbose_name="Миниатюра",
    )
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=10,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество на складе",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
    )

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Товар",
    )
    image = models.ImageField(
        upload_to="products/gallery/",
        verbose_name="Изображение",
    )
    thumbnail = models.ImageField(
        upload_to="products/gallery/thumbnails/",
        blank=True,
        null=True,
        editable=False,
        verbose_name="Миниатюра",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
    )

    def __str__(self):
        return f"Изображение товара: {self.product.name}"

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def save(self, *args, **kwargs):
        if self.image and not self.image._committed:
            original_name = Path(self.image.name).stem

            original, thumbnail = process_image(self.image)

            self.image.save(
                f"{original_name}.jpg",
                original,
                save=False,
            )
            self.thumbnail.save(
                f"{original_name}_thumb.jpg",
                thumbnail,
                save=False,
            )

        super().save(*args, **kwargs)


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "новый"
        PAID = "paid", "Оплачен"
        SHIPPED = "shipped", "Отправвлен"
        CANCELLED = "cancelled", "Отменен"

    customer = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Покупатель",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Заказ №{self.pk}"

    @property
    def total_sum(self):
        return sum(
            (item.price * item.quantity for item in self.items.all()),
            start=Decimal("0.00"),
        )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена на момент заказа'
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self) -> str:
        return f'{self.product.name} * {self.quantity}'
    