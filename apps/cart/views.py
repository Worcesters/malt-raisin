from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.cart.selectors import get_cart_item_count, get_or_create_cart
from apps.cart.services import add_to_cart, remove_cart_item, update_cart_item


def _render_cart_after_mutation(request: HttpRequest) -> HttpResponse:
    """Reaffiche le panier ; en HTMX, inclut les swaps OOB pour le compteur navbar."""
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product").all()
    tpl = "cart/partials/cart_sidebar.html" if request.htmx else "cart/cart_detail.html"
    return render(
        request,
        tpl,
        {
            "cart": cart,
            "items": items,
            "update_nav_cart_count": bool(request.htmx),
        },
    )


class CartDetailView(View):
    """Affiche le panier complet."""

    def get(self, request) -> HttpResponse:
        cart = get_or_create_cart(request)
        items = cart.items.select_related("product").all()
        return render(request, "cart/cart_detail.html", {"cart": cart, "items": items})


class CartAddView(View):
    """Ajoute un produit au panier (POST uniquement)."""

    def post(self, request, product_id: int) -> HttpResponse:
        quantity = int(request.POST.get("quantity", 1))
        add_to_cart(request, product_id, quantity)
        if request.htmx:
            return render(
                request,
                "cart/partials/add_to_cart_response.html",
                {"cart_count": get_cart_item_count(request)},
            )
        return redirect("cart:detail")


class CartUpdateView(View):
    """Met à jour la quantité d'un article du panier (POST uniquement)."""

    def post(self, request, item_id: int) -> HttpResponse:
        quantity = int(request.POST.get("quantity", 1))
        update_cart_item(item_id, quantity)
        return _render_cart_after_mutation(request)


class CartRemoveView(View):
    """Supprime un article du panier (POST uniquement)."""

    def post(self, request, item_id: int) -> HttpResponse:
        remove_cart_item(item_id)
        return _render_cart_after_mutation(request)
