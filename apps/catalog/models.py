from django.db import models
from django.urls import reverse


class AlcoholType(models.TextChoices):
    VIN = "vin", "Vin"
    BIERE = "biere", "Bière"
    WHISKY = "whisky", "Whisky"
    RHUM = "rhum", "Rhum"
    VODKA = "vodka", "Vodka"
    GIN = "gin", "Gin"
    CHAMPAGNE = "champagne", "Champagne"
    AUTRE = "autre", "Autre"


class Category(models.Model):
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Description", blank=True)
    image = models.ImageField("Image", upload_to="categories/", blank=True)
    order = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField("Nom", max_length=300)
    slug = models.SlugField("Slug", unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Catégorie",
    )
    description = models.TextField("Description", blank=True)
    price = models.DecimalField("Prix (€)", max_digits=8, decimal_places=2)
    image = models.ImageField("Image", upload_to="products/", blank=True)
    alcohol_type = models.CharField(
        "Type d'alcool",
        max_length=20,
        choices=AlcoholType.choices,
        default=AlcoholType.VIN,
    )
    volume = models.CharField("Volume", max_length=20, blank=True, help_text="Ex: 75cl, 70cl")
    alcohol_degree = models.DecimalField(
        "Degré d'alcool (%)",
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    origin = models.CharField("Origine", max_length=200, blank=True)
    stock = models.PositiveIntegerField("Stock", default=0)
    is_featured = models.BooleanField("Mis en avant", default=False)
    is_active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})

    @property
    def in_stock(self) -> bool:
        return self.stock > 0
