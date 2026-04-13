from rest_framework import serializers

from apps.events.models import Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "slug", "image", "event_date", "location"]


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id", "title", "slug", "description", "image",
            "event_date", "location", "created_at",
        ]
