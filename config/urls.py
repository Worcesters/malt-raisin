from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("boutique/", include("apps.catalog.urls")),
    path("panier/", include("apps.cart.urls")),
    path("commande/", include("apps.orders.urls")),
    path("compte/", include("apps.accounts.urls")),
    path("evenements/", include("apps.events.urls")),
    path("contact/", include("apps.contact.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
