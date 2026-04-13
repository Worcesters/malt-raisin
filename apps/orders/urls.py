from django.urls import path

from apps.orders import views

app_name = "orders"

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("confirmation/<int:order_id>/", views.order_confirmation, name="confirmation"),
    path("paypal/create/", views.paypal_create_order, name="paypal_create"),
    path("paypal/capture/", views.paypal_capture_order, name="paypal_capture"),
]
