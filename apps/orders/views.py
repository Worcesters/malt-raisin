import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.cart.selectors import get_or_create_cart
from apps.orders.forms import CheckoutForm
from apps.orders.selectors import get_order_detail
from apps.orders.services import confirm_order, create_order_from_cart


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product").all()

    if not items.exists():
        return redirect("cart:detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = create_order_from_cart(
                user=request.user,
                cart=cart,
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                phone=data.get("phone", ""),
                address=data["address"],
                city=data["city"],
                postal_code=data["postal_code"],
            )
            request.session["pending_order_id"] = order.pk
            return render(request, "orders/payment.html", {
                "order": order,
                "paypal_client_id": settings.PAYPAL_CLIENT_ID,
            })
    else:
        form = CheckoutForm(initial={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "phone": getattr(request.user, "phone", ""),
            "address": getattr(request.user, "address", ""),
            "city": getattr(request.user, "city", ""),
            "postal_code": getattr(request.user, "postal_code", ""),
        })

    return render(request, "orders/checkout.html", {
        "form": form,
        "cart": cart,
        "items": items,
    })


@login_required
def order_confirmation(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_order_detail(order_id, request.user)
    if order is None:
        return redirect("core:home")
    return render(request, "orders/confirmation.html", {"order": order})


@require_POST
@login_required
def paypal_create_order(request: HttpRequest) -> JsonResponse:
    order_id = request.session.get("pending_order_id")
    if not order_id:
        return JsonResponse({"error": "No pending order"}, status=400)
    order = get_order_detail(order_id, request.user)
    if order is None:
        return JsonResponse({"error": "Order not found"}, status=404)
    return JsonResponse({"id": str(order.pk), "amount": str(order.total)})


@require_POST
@login_required
def paypal_capture_order(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    paypal_order_id = data.get("orderID", "")
    order_id = request.session.get("pending_order_id")

    if not order_id:
        return JsonResponse({"error": "No pending order"}, status=400)

    order = get_order_detail(order_id, request.user)
    if order is None:
        return JsonResponse({"error": "Order not found"}, status=404)

    confirm_order(order, paypal_order_id)
    del request.session["pending_order_id"]

    return JsonResponse({"status": "ok", "redirect": f"/commande/confirmation/{order.pk}/"})
