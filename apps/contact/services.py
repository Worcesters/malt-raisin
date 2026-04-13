from django.core.mail import send_mail

from apps.contact.models import ContactMessage


def create_contact_message(
    *,
    name: str,
    email: str,
    subject: str,
    message: str,
) -> ContactMessage:
    msg = ContactMessage.objects.create(
        name=name,
        email=email,
        subject=subject,
        message=message,
    )
    send_mail(
        subject=f"[Malt & Raisin] {subject}",
        message=f"De: {name} <{email}>\n\n{message}",
        from_email=None,
        recipient_list=["contact@maltraisin.fr"],
        fail_silently=True,
    )
    return msg
