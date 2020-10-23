import face_recognition

from face_detection.models import FaceEncoding


def obtain_encodings(image_id, album_id, image_file):
    encodings = _get_encodings(image_file)
    models = []
    for encoding in encodings:
        models.append(_save_encoding(image_id, album_id, encoding))
    return models


def _get_encodings(image_file):
    img = face_recognition.load_image_file(image_file)
    return face_recognition.face_encodings(img)


def _save_encoding(image_id, album_id, encoding):
    encoding_model = FaceEncoding.encoding_to_model(image_id, album_id, encoding)
    encoding_model.save()
    return encoding_model


def search_persons(encoding_pks):
    encodings = []
    for encoding_pk in encoding_pks:
        encodings.append(FaceEncoding.objects.get(pk=encoding_pk).fields_to_encoding())

    matches = []
    for encoding in FaceEncoding.objects.exclude(pk__in=encoding_pks):
        if True in face_recognition.compare_faces(
            encodings, encoding.fields_to_encoding()
        ):
            matches.append(encoding.image_id)

    return set(matches)
