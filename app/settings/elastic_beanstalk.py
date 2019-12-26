import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'NAME': os.environ.get('POSTGRES_DB'),
        'HOST': os.environ.get('DJANGO_POSTGRES_HOST'),
        'PORT': 5432,
    }
}
