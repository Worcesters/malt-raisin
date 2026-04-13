from django.http import HttpResponse
from django.views.generic import TemplateView

from apps.catalog.selectors import get_featured_products
from apps.events.selectors import get_upcoming_events


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        context["featured_products"] = get_featured_products(limit=8)
        context["upcoming_events"] = get_upcoming_events(limit=3)
        return context
