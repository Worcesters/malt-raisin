from django.urls import path

from apps.cart import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("ajouter/<int:product_id>/", views.cart_add, name="add"),
    path("modifier/<int:item_id>/", views.cart_update, name="update"),
    path("supprimer/<int:item_id>/", views.cart_remove, name="remove"),
]
