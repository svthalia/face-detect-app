from django.core.management import BaseCommand

from face_detection.services import detector


class Command(BaseCommand):
    help = "Import the face encodings of an image into the database"

    def add_arguments(self, parser):
        parser.add_argument("image_location", type=str)

    def handle(self, *args, **options):
        print("hallo")
        detector.obtain_encodings(1, options["image_location"])
        print("test")
