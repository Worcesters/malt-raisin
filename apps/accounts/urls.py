from django.urls import path

from apps.accounts.views import (
    LoginView,
    LogoutView,
    OrderHistoryView,
    ProfileView,
    RegisterView,
)

app_name = "accounts"

urlpatterns = [
    path("inscription/", RegisterView.as_view(), name="register"),
    path("connexion/", LoginView.as_view(), name="login"),
    path("deconnexion/", LogoutView.as_view(), name="logout"),
    path("profil/", ProfileView.as_view(), name="profile"),
    path("commandes/", OrderHistoryView.as_view(), name="order_history"),
]
