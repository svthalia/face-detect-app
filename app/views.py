import requests
from django.views.generic import ListView, DetailView
from django.conf import settings

from app.models import Album


class IndexView(ListView):
    template_name = 'app/index.html'
    model = Album
    context_object_name = 'albums'


class AlbumView(DetailView):
    template_name = 'app/album.html'
    model = Album
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = requests.get(
            f'https://thalia.nu/api/v1/photos/albums/{context["album"].pk}',
            headers={
                'Authorization': f'Token {settings.THALIA_API_KEY}'
            }).json()

        context['photos'] = data['photos']

        return context
