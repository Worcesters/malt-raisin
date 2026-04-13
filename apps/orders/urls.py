from django.urls import path

from apps.orders.views import (
    CheckoutView,
    OrderConfirmationView,
    PayPalCaptureOrderView,
    PayPalCreateOrderView,
)

app_name = "orders"

urlpatterns = [
    path("", CheckoutView.as_view(), name="checkout"),
    path("confirmation/<int:order_id>/", OrderConfirmationView.as_view(), name="confirmation"),
    path("paypal/create/", PayPalCreateOrderView.as_view(), name="paypal_create"),
    path("paypal/capture/", PayPalCaptureOrderView.as_view(), name="paypal_capture"),
]
