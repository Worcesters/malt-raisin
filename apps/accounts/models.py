from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ) -> "User":
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Un superuser doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Un superuser doit avoir is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True)
    first_name = models.CharField("Prénom", max_length=150, blank=True)
    last_name = models.CharField("Nom", max_length=150, blank=True)
    is_staff = models.BooleanField("Équipe", default=False)
    is_active = models.BooleanField("Actif", default=True)
    date_joined = models.DateTimeField("Date d'inscription", auto_now_add=True)

    phone = models.CharField("Téléphone", max_length=20, blank=True)
    address = models.TextField("Adresse", blank=True)
    city = models.CharField("Ville", max_length=100, blank=True)
    postal_code = models.CharField("Code postal", max_length=10, blank=True)
    newsletter = models.BooleanField("Newsletter", default=False)
    birth_date = models.DateField("Date de naissance", null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self) -> str:
        return self.get_full_name() or self.email

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        return self.first_name
