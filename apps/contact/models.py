from django.db import models


class ContactMessage(models.Model):
    name = models.CharField("Nom", max_length=200)
    email = models.EmailField("Email")
    subject = models.CharField("Sujet", max_length=300)
    message = models.TextField("Message")
    is_read = models.BooleanField("Lu", default=False)
    created_at = models.DateTimeField("Envoyé le", auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.subject} — {self.name}"
