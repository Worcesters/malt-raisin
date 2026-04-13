from django.http import Http404
from django.views.generic import DetailView, ListView

from apps.events.models import Event
from apps.events.selectors import get_event_by_slug, get_published_events


class EventListView(ListView):
    """
    MRO: EventListView -> ListView -> MultipleObjectTemplateResponseMixin
         -> TemplateResponseMixin -> BaseListView -> MultipleObjectMixin
         -> ContextMixin -> View
    """
    template_name = "events/event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        return get_published_events()


class EventDetailView(DetailView):
    """
    MRO: EventDetailView -> DetailView -> SingleObjectTemplateResponseMixin
         -> TemplateResponseMixin -> BaseDetailView -> SingleObjectMixin
         -> ContextMixin -> View
    """
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_object(self, queryset=None) -> Event:
        event = get_event_by_slug(self.kwargs["slug"])
        if event is None:
            raise Http404
        return event
