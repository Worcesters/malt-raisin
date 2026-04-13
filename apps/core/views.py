from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.catalog.selectors import get_featured_products
from apps.events.selectors import get_upcoming_events


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html", {
        "featured_products": get_featured_products(limit=8),
        "upcoming_events": get_upcoming_events(limit=3),
    })
