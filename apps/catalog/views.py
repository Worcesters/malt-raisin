from django.http import Http404, HttpResponse
from django.views.generic import DetailView, ListView

from apps.catalog.models import AlcoholType, Product
from apps.catalog.selectors import filter_products, get_all_categories, get_product_by_slug


class ProductListView(ListView):
    """
    MRO: ProductListView -> ListView -> MultipleObjectTemplateResponseMixin
         -> TemplateResponseMixin -> BaseListView -> MultipleObjectMixin
         -> ContextMixin -> View
    """
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        return filter_products(
            category=self.request.GET.get("category", ""),
            alcohol_type=self.request.GET.get("type", ""),
            search=self.request.GET.get("q", ""),
            sort=self.request.GET.get("sort", ""),
        )

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return ["catalog/partials/product_grid.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        context["categories"] = get_all_categories()
        context["alcohol_types"] = AlcoholType.choices
        context["current_category"] = self.request.GET.get("category", "")
        context["current_type"] = self.request.GET.get("type", "")
        context["current_search"] = self.request.GET.get("q", "")
        context["current_sort"] = self.request.GET.get("sort", "")
        return context


class ProductDetailView(DetailView):
    """
    MRO: ProductDetailView -> DetailView -> SingleObjectTemplateResponseMixin
         -> TemplateResponseMixin -> BaseDetailView -> SingleObjectMixin
         -> ContextMixin -> View
    """
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None) -> Product:
        product = get_product_by_slug(self.kwargs["slug"])
        if product is None:
            raise Http404
        return product
