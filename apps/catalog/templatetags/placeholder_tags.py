from django import template
from django.templatetags.static import static

register = template.Library()

PRODUCT_PLACEHOLDERS: dict[str, str] = {
    "vin": "img/placeholders/vin.svg",
    "biere": "img/placeholders/biere.svg",
    "whisky": "img/placeholders/whisky.svg",
    "rhum": "img/placeholders/rhum.svg",
    "champagne": "img/placeholders/champagne.svg",
    "gin": "img/placeholders/gin.svg",
    "vodka": "img/placeholders/vodka.svg",
    "autre": "img/placeholders/autre.svg",
}


@register.simple_tag
def product_placeholder(alcohol_type: str = "") -> str:
    path = PRODUCT_PLACEHOLDERS.get(alcohol_type, "img/placeholders/autre.svg")
    return static(path)


@register.simple_tag
def event_placeholder() -> str:
    return static("img/placeholders/event.svg")


@register.simple_tag
def category_placeholder() -> str:
    return static("img/placeholders/category.svg")
