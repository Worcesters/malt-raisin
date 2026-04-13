from django.http import HttpRequest


def cart_count(request: HttpRequest) -> dict[str, int]:
    from apps.cart.selectors import get_cart_item_count
    return {"cart_count": get_cart_item_count(request)}
