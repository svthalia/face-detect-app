from django.forms import ImageField, Form


class UserEncodingCreateForm(Form):
    upload_image = ImageField(
        label='Image',
    )

