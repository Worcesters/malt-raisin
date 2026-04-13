from django.http import HttpRequest

from apps.cart.models import Cart, CartItem
from apps.cart.selectors import get_or_create_cart
from apps.catalog.models import Product


def add_to_cart(request: HttpRequest, product_id: int, quantity: int = 1) -> CartItem:
    cart = get_or_create_cart(request)
    product = Product.objects.get(pk=product_id)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity},
    )
    if not created:
        item.quantity += quantity
        item.save()
    return item


def update_cart_item(item_id: int, quantity: int) -> CartItem | None:
    try:
        item = CartItem.objects.get(pk=item_id)
        if quantity <= 0:
            item.delete()
            return None
        item.quantity = quantity
        item.save()
        return item
    except CartItem.DoesNotExist:
        return None


def remove_cart_item(item_id: int) -> None:
    CartItem.objects.filter(pk=item_id).delete()


def clear_cart(cart: Cart) -> None:
    cart.items.all().delete()


def merge_session_cart_to_user(request: HttpRequest) -> None:
    """Fusionne le panier de session anonyme vers le panier utilisateur après connexion."""
    session_key = request.session.session_key
    if not session_key or not request.user.is_authenticated:
        return

    try:
        session_cart = Cart.objects.get(session_key=session_key, user=None)
    except Cart.DoesNotExist:
        return

    user_cart, _ = Cart.objects.get_or_create(user=request.user)

    for item in session_cart.items.select_related("product").all():
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=item.product,
            defaults={"quantity": item.quantity},
        )
        if not created:
            user_item.quantity += item.quantity
            user_item.save()

    session_cart.delete()
