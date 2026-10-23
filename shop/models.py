from django.db import models

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
