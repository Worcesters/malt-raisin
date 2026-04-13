from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.accounts.forms import LoginForm, ProfileForm, RegisterForm
from apps.accounts.services import register_user, update_profile
from apps.cart.services import merge_session_cart_to_user
from apps.orders.selectors import get_user_orders


class RegisterView(View):
    """Inscription utilisateur."""

    def get(self, request) -> HttpResponse:
        return render(request, "accounts/register.html", {"form": RegisterForm()})

    def post(self, request) -> HttpResponse:
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = register_user(
                email=data["email"],
                password=data["password1"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                newsletter=data.get("newsletter", False),
            )
            login(request, user)
            merge_session_cart_to_user(request)
            messages.success(request, "Bienvenue ! Votre compte a été créé.")
            return redirect("core:home")
        return render(request, "accounts/register.html", {"form": form})


class LoginView(View):
    """Connexion utilisateur."""

    def get(self, request) -> HttpResponse:
        return render(request, "accounts/login.html", {"form": LoginForm()})

    def post(self, request) -> HttpResponse:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                merge_session_cart_to_user(request)
                messages.success(request, f"Bonjour {user.first_name or user.email} !")
                return redirect(request.GET.get("next", "core:home"))
            else:
                messages.error(request, "Identifiants incorrects.")
        return render(request, "accounts/login.html", {"form": form})


class LogoutView(View):
    """Déconnexion utilisateur."""

    def get(self, request) -> HttpResponse:
        logout(request)
        messages.info(request, "Vous avez été déconnecté.")
        return redirect("core:home")


class ProfileView(LoginRequiredMixin, View):
    """Profil utilisateur avec mise à jour."""

    def get(self, request) -> HttpResponse:
        form = ProfileForm(instance=request.user)
        return render(request, "accounts/profile.html", {"form": form})

    def post(self, request) -> HttpResponse:
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            data = form.cleaned_data
            update_profile(
                user=request.user,
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                phone=data.get("phone", ""),
                address=data.get("address", ""),
                city=data.get("city", ""),
                postal_code=data.get("postal_code", ""),
                newsletter=data.get("newsletter", False),
            )
            messages.success(request, "Profil mis à jour.")
            return redirect("accounts:profile")
        return render(request, "accounts/profile.html", {"form": form})


class OrderHistoryView(LoginRequiredMixin, View):
    """Historique des commandes."""

    def get(self, request) -> HttpResponse:
        orders = get_user_orders(request.user)
        return render(request, "accounts/order_history.html", {"orders": orders})
