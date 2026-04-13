from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        null=True,
        blank=True,
        verbose_name="Utilisateur",
    )
    session_key = models.CharField("Clé de session", max_length=40, blank=True, db_index=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self) -> str:
        if self.user:
            return f"Panier de {self.user}"
        return f"Panier anonyme ({self.session_key[:8]})"

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items.select_related("product").all())

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.CASCADE,
        verbose_name="Produit",
    )
    quantity = models.PositiveIntegerField("Quantité", default=1)

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = [("cart", "product")]

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name}"

    @property
    def subtotal(self) -> float:
        return float(self.product.price) * self.quantity
