import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

PASSWORD_RULES: list[tuple[str, str]] = [
    (r".{12,}", "12 caractères minimum"),
    (r"[A-Z]", "une majuscule"),
    (r"[a-z]", "une minuscule"),
    (r"\d", "un chiffre"),
    (r"[^A-Za-z0-9]", "un caractère spécial (!@#…)"),
]


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    newsletter = serializers.BooleanField(required=False, default=False)

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def validate_password1(self, value: str) -> str:
        for pattern, label in PASSWORD_RULES:
            if not re.search(pattern, value):
                raise serializers.ValidationError(f"Le mot de passe doit contenir {label}.")
        validate_password(value)
        return value

    def validate(self, data: dict) -> dict:
        if data.get("password1") != data.get("password2"):
            raise serializers.ValidationError({"password2": "Les mots de passe ne correspondent pas."})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email", "phone",
            "address", "city", "postal_code", "newsletter",
        ]
        read_only_fields = ["email"]
