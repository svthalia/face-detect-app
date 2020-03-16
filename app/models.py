from django.conf import settings
from django.db.models import Model, TextField, ForeignKey, CASCADE

from face_detection.models import FaceEncoding


class Album(Model):
    name = TextField()


class UserEncoding(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    encoding = ForeignKey(FaceEncoding, on_delete=CASCADE)
    description = TextField(blank=True, null=True, max_length=100)
