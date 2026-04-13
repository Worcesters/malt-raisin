from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.contact.forms import ContactForm
from apps.contact.services import create_contact_message


def contact_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            create_contact_message(**form.cleaned_data)
            messages.success(request, "Votre message a bien été envoyé. Nous vous répondrons rapidement.")
            return redirect("contact:contact")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})
