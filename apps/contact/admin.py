from django.contrib import admin

from apps.contact.models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["subject", "name", "email", "is_read", "created_at"]
    list_filter = ["is_read", "created_at"]
    list_editable = ["is_read"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["name", "email", "subject", "message", "created_at"]
