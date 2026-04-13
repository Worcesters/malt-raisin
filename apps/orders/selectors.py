from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.orders.models import Order

User = get_user_model()


def get_user_orders(user: "User") -> QuerySet[Order]:
    return Order.objects.filter(user=user).prefetch_related("items__product")


def get_order_detail(order_id: int, user: "User") -> Order | None:
    try:
        return (
            Order.objects.prefetch_related("items__product")
            .get(pk=order_id, user=user)
        )
    except Order.DoesNotExist:
        return None
