# Generated manually – User model sans username (AbstractBaseUser)

import apps.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False, verbose_name="superuser status")),
                ("email", models.EmailField(max_length=254, unique=True, verbose_name="Email")),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="Prénom")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="Nom")),
                ("is_staff", models.BooleanField(default=False, verbose_name="Équipe")),
                ("is_active", models.BooleanField(default=True, verbose_name="Actif")),
                ("date_joined", models.DateTimeField(auto_now_add=True, verbose_name="Date d\u2019inscription")),
                ("phone", models.CharField(blank=True, max_length=20, verbose_name="Téléphone")),
                ("address", models.TextField(blank=True, verbose_name="Adresse")),
                ("city", models.CharField(blank=True, max_length=100, verbose_name="Ville")),
                ("postal_code", models.CharField(blank=True, max_length=10, verbose_name="Code postal")),
                ("newsletter", models.BooleanField(default=False, verbose_name="Newsletter")),
                ("birth_date", models.DateField(blank=True, null=True, verbose_name="Date de naissance")),
                ("groups", models.ManyToManyField(blank=True, related_name="user_set", related_query_name="user", to="auth.group", verbose_name="groups")),
                ("user_permissions", models.ManyToManyField(blank=True, related_name="user_set", related_query_name="user", to="auth.permission", verbose_name="user permissions")),
            ],
            options={
                "verbose_name": "Utilisateur",
                "verbose_name_plural": "Utilisateurs",
            },
            managers=[
                ("objects", apps.accounts.models.UserManager()),
            ],
        ),
    ]
