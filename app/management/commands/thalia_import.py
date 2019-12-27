import requests
from django.core.management import BaseCommand

from app.models import Album
from face_detection.models import FaceEncoding
from face_detection.services import detector


class Command(BaseCommand):
    help = 'Import the face encodings of an image into the database'

    def add_arguments(self, parser):
        parser.add_argument('token', type=str)

    def handle(self, *args, **options):
        Album.objects.all().delete()
        FaceEncoding.objects.all().delete()

        headers = {
            'Authorization': f'Token {options["token"]}'
        }
        albums = requests.get(
            'https://thalia.nu/api/v1/photos/albums',
            headers=headers)

        for album in albums.json():
            Album.objects.create(
                pk=album['pk'],
                name=album['title']
            )

            album = requests.get(
                f'https://thalia.nu/api/v1/photos/albums/{album["pk"]}',
                headers=headers).json()

            for photo in album['photos']:
                detector.obtain_encodings(
                    photo['pk'],
                    requests.get(photo['file']['large'], stream=True).raw
                )
