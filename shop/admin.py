from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem
from django.utils.html import format_html


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "created_at")
    search_fields = ("name", "description")
    list_filter = ("created_at",)
    ordering = ("name",)
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "created_at")
    list_filter = ("created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price", "line_total")
    fields = ("product", "quantity", "price", "line_total")

    @admin.display(description="Сумма позиции")
    def line_total(self, obj):
        if obj.pk:
            return obj.price * obj.quantity
        return "-"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created_at", "total_sum")
    list_filter = ("status", "created_at")
    search_fields = ("customer__email",)
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "updated_at", "total_sum")

    @admin.display(description="Общая сумма заказа")
    def total_sum(self, obj):
        return obj.total_sum
