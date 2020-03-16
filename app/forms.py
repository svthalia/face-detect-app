from django.forms import ImageField, Form, CharField


class UserEncodingCreateForm(Form):
    upload_image = ImageField(
        label='Image',
    )

    description = CharField(
        label='Description',
        max_length=100,
    )

