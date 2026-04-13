from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("inscription/", views.register_view, name="register"),
    path("connexion/", views.login_view, name="login"),
    path("deconnexion/", views.logout_view, name="logout"),
    path("profil/", views.profile_view, name="profile"),
    path("commandes/", views.order_history_view, name="order_history"),
]
