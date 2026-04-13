from datetime import datetime

from apps.events.models import Event


def create_event(
    *,
    title: str,
    slug: str,
    description: str,
    event_date: datetime,
    location: str = "",
    is_published: bool = False,
) -> Event:
    return Event.objects.create(
        title=title,
        slug=slug,
        description=description,
        event_date=event_date,
        location=location,
        is_published=is_published,
    )


def update_event(event: Event, **kwargs: object) -> Event:
    for key, value in kwargs.items():
        setattr(event, key, value)
    event.save()
    return event


def publish_event(event: Event) -> Event:
    event.is_published = True
    event.save(update_fields=["is_published", "updated_at"])
    return event
