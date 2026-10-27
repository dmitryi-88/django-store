
from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem


class StockAvailabilityFilter(admin.SimpleListFilter):
    title = "Наличие на складе"
    parameter_name = "stock_status"

    def lookups(self, request, model_admin):
        return (
            ("in_stock", "В наличии"),
            ("out_of_stock", "Нет в наличии"),
        )

    def queryset(self, request, queryset):
        if self.value() == "in_stock":
            return queryset.filter(stock__gt=0)
        if self.value() == "out_of_stock":
            return queryset.filter(stock=0)
        return queryset


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "created_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", StockAvailabilityFilter)
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

    actions = (
        "mark_as_paid",
        "mark_as_shipped",
        "mark_as_cancelled",
    )

    @admin.display(description="Общая сумма заказа")
    def total_sum(self, obj):
        return obj.total_sum

    def change_selected_status(self, request, queryset, new_status):
        updated_count = 0

        for order in queryset:
            old_status = order.get_status_display()

            if order.status == new_status:
                continue

            order.status = new_status
            order.save(update_fields=("status", "updated_at"))

            new_status_display = order.get_status_display()
            self.log_change(
                request,
                order,
                f"Статус заказа изменён: {old_status} → {new_status_display}",
            )
            updated_count += 1

        self.message_user(
            request,
            f"Изменён статус заказов: {updated_count}.",
        )

    @admin.action(description="Отметить выбранные заказы как оплаченные")
    def mark_as_paid(self, request, queryset):
        self.change_selected_status(
            request,
            queryset,
            Order.Status.PAID,
        )

    @admin.action(description="Отметить выбранные заказы как отправленные")
    def mark_as_shipped(self, request, queryset):
        self.change_selected_status(
            request,
            queryset,
            Order.Status.SHIPPED,
        )

    @admin.action(description="Отменить выбранные заказы")
    def mark_as_cancelled(self, request, queryset):
        self.change_selected_status(
            request,
            queryset,
            Order.Status.CANCELLED,
        )
