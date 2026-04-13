import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

PASSWORD_RULES: list[tuple[str, str]] = [
    (r".{12,}", "12 caractères minimum"),
    (r"[A-Z]", "une majuscule"),
    (r"[a-z]", "une minuscule"),
    (r"\d", "un chiffre"),
    (r"[^A-Za-z0-9]", "un caractère spécial (!@#…)"),
]


class RegisterForm(forms.Form):
    first_name = forms.CharField(label="Prénom", max_length=100)
    last_name = forms.CharField(label="Nom", max_length=100)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)
    newsletter = forms.BooleanField(label="S'inscrire à la newsletter", required=False)

    def clean_email(self) -> str:
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_password1(self) -> str:
        password = self.cleaned_data["password1"]
        for pattern, label in PASSWORD_RULES:
            if not re.search(pattern, password):
                raise forms.ValidationError(f"Le mot de passe doit contenir {label}.")
        validate_password(password)
        return password

    def clean(self) -> dict:
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Les mots de passe ne correspondent pas.")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "postal_code",
            "newsletter",
        ]
