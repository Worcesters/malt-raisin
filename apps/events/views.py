from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from apps.events.selectors import get_event_by_slug, get_published_events


def event_list(request: HttpRequest) -> HttpResponse:
    events = get_published_events()
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request: HttpRequest, slug: str) -> HttpResponse:
    event = get_event_by_slug(slug)
    if event is None:
        raise Http404
    return render(request, "events/event_detail.html", {"event": event})
