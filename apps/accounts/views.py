from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.accounts.forms import LoginForm, ProfileForm, RegisterForm
from apps.accounts.services import register_user, update_profile
from apps.cart.services import merge_session_cart_to_user
from apps.orders.selectors import get_user_orders


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
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
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
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
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect("core:home")


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
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
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


@login_required
def order_history_view(request: HttpRequest) -> HttpResponse:
    orders = get_user_orders(request.user)
    return render(request, "accounts/order_history.html", {"orders": orders})
