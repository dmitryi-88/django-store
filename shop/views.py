from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .cart import Cart
from .models import Product, Order, OrderItem


def product_list(request):
    products = Product.objects.all()

    templ = "shop/product_list.html"
    data = {"products": products}

    return render(request, templ, data)


def cart_detail(request):
    cart = Cart(request)

    templ = "shop/cart/detail.html"
    data = {"cart": cart}

    return render(request, templ, data)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if cart.add(product):
        messages.success(request, "Товар добавлен в корзину.")
    else:
        messages.error(
            request,
            f"Недостаточно товара на складе: {product.name}. "
            f"В наличии: {product.stock}.",
        )

    return redirect("shop:product_list")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect("shop:cart_detail")


@login_required
@require_POST
def checkout(request):
    cart = Cart(request)

    if not cart.cart:
        messages.error(request, "Корзина пуста")
        return redirect("shop:cart_detail")

    with transaction.atomic():
        products = Product.objects.select_for_update().filter(pk__in=cart.cart.keys())

        products_by_id = {str(product.pk): product for product in products}

        if len(products_by_id) != len(cart.cart):
            messages.error(
                request,
                "Некоторые товары больше недоступны.",
            )
            return redirect("shop:cart_detail")

        # Проверяем остатки до создания заказа.
        for product_id, item in cart.cart.items():
            product = products_by_id[product_id]
            quantity = item["quantity"]

            if quantity <= 0 or quantity > product.stock:
                messages.error(
                    request,
                    f"Недостаточно товара «{product.name}». "
                    f"В наличии: {product.stock}.",
                )
                return redirect("shop:cart_detail")

        # Создаём заказ.
        order = Order.objects.create(
            customer=request.user,
        )

        # Создаём позиции заказа и уменьшаем остатки.
        for product_id, item in cart.cart.items():
            product = products_by_id[product_id]
            quantity = item["quantity"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

            product.stock -= quantity
            product.save(update_fields=["stock"])

    # Очищаем корзину только после успешной транзакции.
    cart.clear()

    messages.success(
        request,
        f"Заказ №{order.pk} успешно оформлен.",
    )

    return redirect("shop:cart_detail")
