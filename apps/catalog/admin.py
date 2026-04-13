from django.contrib import admin

from apps.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "alcohol_type", "stock", "is_featured", "is_active"]
    list_filter = ["category", "alcohol_type", "is_featured", "is_active"]
    list_editable = ["price", "stock", "is_featured", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]
