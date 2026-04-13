from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.contact.forms import ContactForm
from apps.contact.services import create_contact_message


class ContactView(View):
    """Page de contact avec formulaire."""

    def get(self, request) -> HttpResponse:
        return render(request, "contact/contact.html", {"form": ContactForm()})

    def post(self, request) -> HttpResponse:
        form = ContactForm(request.POST)
        if form.is_valid():
            create_contact_message(**form.cleaned_data)
            messages.success(request, "Votre message a bien été envoyé. Nous vous répondrons rapidement.")
            return redirect("contact:contact")
        return render(request, "contact/contact.html", {"form": form})
