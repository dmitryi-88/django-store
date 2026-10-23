from django.contrib import admin
from .models import Category, News


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "created_at",
    )
    list_filter = ("category", "created_at")
    search_fields = ("title", "content", "author__email")
    list_select_related = ("category", "author")
