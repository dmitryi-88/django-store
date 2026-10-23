from django.contrib import admin

from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "owner", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "description", "owner__email")
    ordering = ("-created_at",)
