from config.settings.base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

# --- Email (console en dev) --------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
