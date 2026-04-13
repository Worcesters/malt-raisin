from django.db import models
from django.urls import reverse


class Event(models.Model):
    title = models.CharField("Titre", max_length=300)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="events/", blank=True)
    event_date = models.DateTimeField("Date de l'événement")
    location = models.CharField("Lieu", max_length=300, blank=True)
    is_published = models.BooleanField("Publié", default=False)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ["event_date"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("events:event_detail", kwargs={"slug": self.slug})
