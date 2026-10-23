from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(BaseModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "категории"

    name = models.CharField(
        verbose_name="Название",
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class News(BaseModel):
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]
        permissions = [
            ("can_edit_others_news", "Может редактировать чужие новости"),
            ("can_delete_others_news", "Может удалять чужие новости"),
        ]

    title = models.CharField(
        verbose_name="Заголовок",
        max_length=100,
    )
    content = models.TextField(verbose_name="Содержание")
    category = models.ForeignKey(
        verbose_name="Категория",
        to=Category,
        on_delete=models.PROTECT,
        related_name="news",
    )
    author = models.ForeignKey(
        verbose_name="Автор",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="news",
    )
