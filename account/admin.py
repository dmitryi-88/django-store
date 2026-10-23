from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import EmailUser, UserProfile


@admin.register(EmailUser)
class EmailUserAdmin(UserAdmin):
    model = EmailUser

    list_display = ("email", "is_staff", "is_active", "is_superuser")
    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Даты",
            {"fields": ("last_login",)},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city")
    search_fields = ("user__email", "city")
