from rest_framework import serializers

from apps.cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", max_digits=8, decimal_places=2, read_only=True,
    )
    product_image = serializers.ImageField(source="product.image", read_only=True)
    product_alcohol_type = serializers.CharField(source="product.alcohol_type", read_only=True)
    subtotal = serializers.FloatField(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id", "product_id", "product_name", "product_slug",
            "product_price", "product_image", "product_alcohol_type",
            "quantity", "subtotal",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.FloatField(read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "total", "item_count"]


class AddToCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, default=1)
