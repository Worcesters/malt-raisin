from django.http import HttpRequest

from apps.cart.models import Cart


def get_or_create_cart(request: HttpRequest) -> Cart:
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


def get_cart_item_count(request: HttpRequest) -> int:
    if request.user.is_authenticated:
        try:
            return request.user.cart.item_count
        except Cart.DoesNotExist:
            return 0

    session_key = request.session.session_key
    if not session_key:
        return 0

    try:
        cart = Cart.objects.get(session_key=session_key, user=None)
        return cart.item_count
    except Cart.DoesNotExist:
        return 0
