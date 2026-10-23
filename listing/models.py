from django.db import models
from django.conf import settings


class Listing(models.Model):
    class Meta:
        verbose_name = "объявление"
        verbose_name_plural = "объявления"
        permissions = [
            ("can_moderate_listing", "право редактировать чужое объявление"),
            ("can_moderate_self_listing", "право редактировать свое объявление"),
        ]

    title = models.CharField(
        verbose_name="заголовок",
        max_length=255,
    )
    description = models.TextField(
        verbose_name="описание",
    )
    price = models.DecimalField(
        verbose_name="цена",
        max_digits=10,
        decimal_places=2,
    )
    owner = models.ForeignKey(
        verbose_name="автор",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
