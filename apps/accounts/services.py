from django.contrib.auth import get_user_model

User = get_user_model()


def register_user(
    *,
    email: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
    newsletter: bool = False,
) -> "User":
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        newsletter=newsletter,
    )
    return user


def update_profile(
    *,
    user: "User",
    first_name: str,
    last_name: str,
    email: str,
    phone: str = "",
    address: str = "",
    city: str = "",
    postal_code: str = "",
    newsletter: bool = False,
) -> "User":
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.phone = phone
    user.address = address
    user.city = city
    user.postal_code = postal_code
    user.newsletter = newsletter
    user.save()
    return user
