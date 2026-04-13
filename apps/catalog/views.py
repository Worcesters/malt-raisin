from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.catalog.models import AlcoholType
from apps.catalog.selectors import filter_products, get_all_categories, get_product_by_slug


def product_list(request: HttpRequest) -> HttpResponse:
    category = request.GET.get("category", "")
    alcohol_type = request.GET.get("type", "")
    search = request.GET.get("q", "")
    sort = request.GET.get("sort", "")

    products = filter_products(
        category=category,
        alcohol_type=alcohol_type,
        search=search,
        sort=sort,
    )

    context = {
        "products": products,
        "categories": get_all_categories(),
        "alcohol_types": AlcoholType.choices,
        "current_category": category,
        "current_type": alcohol_type,
        "current_search": search,
        "current_sort": sort,
    }

    if request.htmx:
        return render(request, "catalog/partials/product_grid.html", context)
    return render(request, "catalog/product_list.html", context)


def product_detail(request: HttpRequest, slug: str) -> HttpResponse:
    product = get_product_by_slug(slug)
    if product is None:
        from django.http import Http404
        raise Http404
    return render(request, "catalog/product_detail.html", {"product": product})
