from django.urls import path

from apps.cart.views import CartAddView, CartDetailView, CartRemoveView, CartUpdateView

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="detail"),
    path("ajouter/<int:product_id>/", CartAddView.as_view(), name="add"),
    path("modifier/<int:item_id>/", CartUpdateView.as_view(), name="update"),
    path("supprimer/<int:item_id>/", CartRemoveView.as_view(), name="remove"),
]
