from django.urls import path

from apps.events.views import EventDetailView, EventListView

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="event_list"),
    path("<slug:slug>/", EventDetailView.as_view(), name="event_detail"),
]
