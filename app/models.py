from django.conf import settings
from django.db.models import Model, TextField, ForeignKey, CASCADE, ManyToManyField

from face_detection.models import FaceEncoding


class Album(Model):
    name = TextField()


class UserEncoding(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    encoding = ForeignKey(FaceEncoding, on_delete=CASCADE)
    description = TextField(blank=True, null=True, max_length=100)

    matches = ManyToManyField(FaceEncoding, related_name="matches")

    def calculate_matches(self):
        encoding = self.encoding.fields_to_encoding()
        distance_function = "sqrt("
        for i in range(0, 128):
            distance_function += f"power(field{i} - {encoding[i]}, 2) + "
        distance_function = distance_function[0:-2] + "),"
        distance_function = distance_function[0:-1]

        matches = (
            FaceEncoding.objects.exclude(album_id=None)
            .order_by("-album_id")
            .extra(where=[f"{distance_function} < 0.49"])
        )

        for match in matches:
            self.matches.add(match)
