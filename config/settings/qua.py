from config.settings.base import *  # noqa: F401, F403

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: v.split(","))  # noqa: F405

# --- Email (SMTP pour la QA) -------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
