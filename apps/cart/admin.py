from django.contrib import admin

from apps.cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ["product", "quantity"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user", "created_at"]
    inlines = [CartItemInline]
