from decimal import Decimal

from django.contrib.auth import get_user_model

from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem, OrderStatus

User = get_user_model()


def create_order_from_cart(
    *,
    user: "User",
    cart: Cart,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    address: str,
    city: str,
    postal_code: str,
) -> Order:
    items = cart.items.select_related("product").all()
    if not items.exists():
        raise ValueError("Le panier est vide.")

    total = Decimal("0.00")
    order = Order.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        address=address,
        city=city,
        postal_code=postal_code,
        total=Decimal("0.00"),
    )

    order_items: list[OrderItem] = []
    for item in items:
        line_total = item.product.price * item.quantity
        total += line_total
        order_items.append(
            OrderItem(
                order=order,
                product=item.product,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.product.price,
            )
        )

    OrderItem.objects.bulk_create(order_items)
    order.total = total
    order.save(update_fields=["total"])

    cart.items.all().delete()
    return order


def confirm_order(order: Order, paypal_order_id: str) -> Order:
    order.paypal_order_id = paypal_order_id
    order.status = OrderStatus.PAID
    order.save(update_fields=["paypal_order_id", "status", "updated_at"])
    return order


def cancel_order(order: Order) -> Order:
    order.status = OrderStatus.CANCELLED
    order.save(update_fields=["status", "updated_at"])
    return order
