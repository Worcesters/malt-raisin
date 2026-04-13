from django.conf import settings
from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = "pending", "En attente"
    PAID = "paid", "Payée"
    PROCESSING = "processing", "En préparation"
    SHIPPED = "shipped", "Expédiée"
    DELIVERED = "delivered", "Livrée"
    CANCELLED = "cancelled", "Annulée"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Utilisateur",
    )
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    total = models.DecimalField("Total (€)", max_digits=10, decimal_places=2)
    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    address = models.TextField("Adresse de livraison")
    city = models.CharField("Ville", max_length=100)
    postal_code = models.CharField("Code postal", max_length=10)
    paypal_order_id = models.CharField("PayPal Order ID", max_length=100, blank=True)
    created_at = models.DateTimeField("Créée le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifiée le", auto_now=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Commande #{self.pk} — {self.get_status_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Produit",
    )
    product_name = models.CharField("Nom du produit", max_length=300)
    quantity = models.PositiveIntegerField("Quantité")
    unit_price = models.DecimalField("Prix unitaire (€)", max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product_name}"

    @property
    def subtotal(self) -> float:
        return float(self.unit_price) * self.quantity
