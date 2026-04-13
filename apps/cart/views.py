from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from apps.cart.selectors import get_or_create_cart
from apps.cart.services import add_to_cart, remove_cart_item, update_cart_item


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product").all()
    return render(request, "cart/cart_detail.html", {"cart": cart, "items": items})


@require_POST
def cart_add(request: HttpRequest, product_id: int) -> HttpResponse:
    quantity = int(request.POST.get("quantity", 1))
    add_to_cart(request, product_id, quantity)
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product").all()

    if request.htmx:
        return render(request, "cart/partials/cart_sidebar.html", {"cart": cart, "items": items})
    return render(request, "cart/cart_detail.html", {"cart": cart, "items": items})


@require_POST
def cart_update(request: HttpRequest, item_id: int) -> HttpResponse:
    quantity = int(request.POST.get("quantity", 1))
    update_cart_item(item_id, quantity)
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product").all()

    if request.htmx:
        return render(request, "cart/partials/cart_sidebar.html", {"cart": cart, "items": items})
    return render(request, "cart/cart_detail.html", {"cart": cart, "items": items})


@require_POST
def cart_remove(request: HttpRequest, item_id: int) -> HttpResponse:
    remove_cart_item(item_id)
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product").all()

    if request.htmx:
        return render(request, "cart/partials/cart_sidebar.html", {"cart": cart, "items": items})
    return render(request, "cart/cart_detail.html", {"cart": cart, "items": items})
