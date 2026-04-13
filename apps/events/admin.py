from django.contrib import admin

from apps.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "event_date", "location", "is_published"]
    list_filter = ["is_published", "event_date"]
    list_editable = ["is_published"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "description"]
