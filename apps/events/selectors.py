from django.db.models import QuerySet
from django.utils import timezone

from apps.events.models import Event


def get_published_events() -> QuerySet[Event]:
    return Event.objects.filter(is_published=True)


def get_upcoming_events(limit: int = 3) -> QuerySet[Event]:
    return get_published_events().filter(event_date__gte=timezone.now())[:limit]


def get_event_by_slug(slug: str) -> Event | None:
    try:
        return get_published_events().get(slug=slug)
    except Event.DoesNotExist:
        return None
