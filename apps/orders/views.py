import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.selectors import get_or_create_cart
from apps.orders.forms import CheckoutForm
from apps.orders.selectors import get_order_detail
from apps.orders.services import confirm_order, create_order_from_cart


class CheckoutView(LoginRequiredMixin, View):
    """
    Tunnel de commande : formulaire d'adresse puis paiement.
    MRO: CheckoutView -> LoginRequiredMixin -> AccessMixin -> View
    """

    def get(self, request) -> HttpResponse:
        cart = get_or_create_cart(request)
        items = cart.items.select_related("product").all()
        if not items.exists():
            return redirect("cart:detail")

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
            "form": form, "cart": cart, "items": items,
        })

    def post(self, request) -> HttpResponse:
        cart = get_or_create_cart(request)
        items = cart.items.select_related("product").all()
        if not items.exists():
            return redirect("cart:detail")

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
        return render(request, "orders/checkout.html", {
            "form": form, "cart": cart, "items": items,
        })


class OrderConfirmationView(LoginRequiredMixin, View):
    """Affiche la confirmation de commande."""

    def get(self, request, order_id: int) -> HttpResponse:
        order = get_order_detail(order_id, request.user)
        if order is None:
            return redirect("core:home")
        return render(request, "orders/confirmation.html", {"order": order})


class PayPalCreateOrderView(APIView):
    """API DRF : crée l'intention de paiement PayPal."""
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        order_id = request.session.get("pending_order_id")
        if not order_id:
            return Response({"error": "No pending order"}, status=status.HTTP_400_BAD_REQUEST)
        order = get_order_detail(order_id, request.user)
        if order is None:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"id": str(order.pk), "amount": str(order.total)})


class PayPalCaptureOrderView(APIView):
    """API DRF : capture le paiement PayPal et confirme la commande."""
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        paypal_order_id = request.data.get("orderID", "")
        order_id = request.session.get("pending_order_id")

        if not order_id:
            return Response({"error": "No pending order"}, status=status.HTTP_400_BAD_REQUEST)

        order = get_order_detail(order_id, request.user)
        if order is None:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        confirm_order(order, paypal_order_id)
        del request.session["pending_order_id"]

        return Response({"status": "ok", "redirect": f"/commande/confirmation/{order.pk}/"})
