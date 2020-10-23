import requests
from django.core.management import BaseCommand

from app.models import Album
from face_detection.models import FaceEncoding
from face_detection.services import detector


class Command(BaseCommand):
    help = "Import the face encodings of an image into the database"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)

    def handle(self, *args, **options):
        last_album = Album.objects.order_by("pk").first()
        if last_album:
            last_album.delete()
            FaceEncoding.objects.filter(album_id=last_album.pk)

        headers = {"Authorization": f'Token {options["token"]}'}
        albums = requests.get("https://thalia.nu/api/v1/photos/albums", headers=headers)

        for album in albums.json():
            if Album.objects.filter(pk=album["pk"]).exists():
                continue

            Album.objects.get_or_create(pk=album["pk"], name=album["title"])

            self.stdout.write(f'Working on {album["pk"]} {album["title"]}')

            album = requests.get(
                f'https://thalia.nu/api/v1/photos/albums/{album["pk"]}', headers=headers
            ).json()

            for photo in album["photos"]:
                FaceEncoding.objects.filter(image_id=photo["pk"]).delete()
                detector.obtain_encodings(
                    photo["pk"],
                    album["pk"],
                    requests.get(photo["file"]["large"], stream=True).raw,
                )
