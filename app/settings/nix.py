import os

COMPRESS_OFFLINE = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": os.environ.get("POSTGRES_USER", "face"),
        "NAME": os.environ.get("POSTGRES_DB", "face"),
    }
}
