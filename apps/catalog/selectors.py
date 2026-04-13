from django.db.models import QuerySet

from apps.catalog.models import Category, Product


def get_all_categories() -> QuerySet[Category]:
    return Category.objects.all()


def get_active_products() -> QuerySet[Product]:
    return Product.objects.filter(is_active=True).select_related("category")


def get_featured_products(limit: int = 8) -> QuerySet[Product]:
    return get_active_products().filter(is_featured=True)[:limit]


def get_products_by_category(category_slug: str) -> QuerySet[Product]:
    return get_active_products().filter(category__slug=category_slug)


def get_products_by_type(alcohol_type: str) -> QuerySet[Product]:
    return get_active_products().filter(alcohol_type=alcohol_type)


def search_products(query: str) -> QuerySet[Product]:
    return get_active_products().filter(name__icontains=query)


def get_product_by_slug(slug: str) -> Product | None:
    try:
        return get_active_products().get(slug=slug)
    except Product.DoesNotExist:
        return None


def filter_products(
    *,
    category: str = "",
    alcohol_type: str = "",
    search: str = "",
    sort: str = "",
) -> QuerySet[Product]:
    qs = get_active_products()
    if category:
        qs = qs.filter(category__slug=category)
    if alcohol_type:
        qs = qs.filter(alcohol_type=alcohol_type)
    if search:
        qs = qs.filter(name__icontains=search)
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "name":
        qs = qs.order_by("name")
    return qs
