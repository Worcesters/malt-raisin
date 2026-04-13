from django.contrib import admin

from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "product_name", "quantity", "unit_price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user", "total", "status", "created_at"]
    list_filter = ["status", "created_at"]
    list_editable = ["status"]
    search_fields = ["user__email", "user__first_name", "user__last_name", "paypal_order_id"]
    inlines = [OrderItemInline]
    readonly_fields = ["paypal_order_id", "created_at", "updated_at"]
