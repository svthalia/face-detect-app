from django.db.models import Model, TextField


class Album(Model):
    name = TextField()
