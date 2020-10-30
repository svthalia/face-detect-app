import os
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import urlparse

import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    FormView,
    TemplateView,
)

from app.cache import albums_cache
from app.forms import UserEncodingCreateForm
from app.models import Album, UserEncoding
from face_detection.models import FaceEncoding
from face_detection.services import detector


class TokenAuth(View):
    def get(self, request, *args, **kwargs):
        if "token" in request.GET:
            response = requests.get(
                f"https://thalia.nu/api/v1/members/me",
                headers={"Authorization": f'Token {request.GET["token"]}'},
            ).json()
            user = User.objects.get(pk=response["pk"])

            login(request, user=user)
            request.session["token"] = request.GET["token"]
        return redirect("index")


@method_decorator(staff_member_required, "dispatch")
@method_decorator(login_required, "dispatch")
class AlbumsIndexView(ListView):
    template_name = "app/albums/index.html"
    model = Album
    context_object_name = "albums"
    ordering = "-pk"


@method_decorator(login_required, "dispatch")
class AlbumsDetailView(DetailView):
    template_name = "app/albums/detail.html"
    model = Album
    context_object_name = "album"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = requests.get(
            f'https://thalia.nu/api/v1/photos/albums/{context["album"].pk}',
            headers={"Authorization": f'Token {self.request.session["token"]}'},
        ).json()

        context["title"] = data["title"]
        context["date"] = data["date"]
        context["photos"] = data["photos"]

        return context


@method_decorator(login_required, "dispatch")
class RandomAlbumView(View):
    def dispatch(self, request, *args, **kwargs):
        album = Album.objects.order_by("?").first()
        return redirect("albums:detail", pk=album.pk)


@method_decorator(login_required, "dispatch")
class MyPhotosView(TemplateView):
    template_name = "app/myphotos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        photos = []
        encodings = FaceEncoding.objects.order_by("-album_id").filter(
            matches__user=self.request.user
        )
        albums = {x.album_id for x in encodings if x.album_id not in albums_cache}

        if encodings.exists():
            s = requests.Session()
            s.headers.update(
                {"Authorization": f'Token {self.request.session["token"]}'}
            )

            def get_url(album_id):
                if album_id not in albums_cache:
                    albums_cache[album_id] = s.get(
                        f"https://thalia.nu/api/v1/photos/albums/{album_id}/"
                    ).json()

            with ThreadPoolExecutor(max_workers=20) as pool:
                pool.map(get_url, albums)
            for encoding in encodings:
                data = albums_cache[encoding.album_id]
                for x in filter(lambda x: x["pk"] == encoding.image_id, data["photos"]):
                    parsed = urlparse(x['file']['full'])
                    split = os.path.split(parsed.path)
                    x.update({
                        'album_name': f"{data['title']} {data['date']}",
                        'download': f"{parsed.scheme}://{parsed.hostname}{split[0].replace('media/private', 'members')}/download/{split[1]}"
                    })
                    photos.append(x)
            s.close()

        context["title"] = "Photos of you"
        context["photos"] = photos
        return context


@method_decorator(login_required, "dispatch")
class UserEncodingIndexView(ListView):
    template_name = "app/encodings/index.html"
    model = UserEncoding
    context_object_name = "encodings"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@method_decorator(login_required, "dispatch")
class UserEncodingCreateView(FormView):
    template_name = "app/encodings/create.html"
    form_class = UserEncodingCreateForm
    success_url = reverse_lazy("encodings:index")

    def form_valid(self, form):
        encodings = detector.obtain_encodings(
            None, None, form.cleaned_data["upload_image"].file
        )

        for encoding in encodings:
            user_enc = UserEncoding.objects.create(
                encoding=encoding,
                description=form.cleaned_data.get("description", ""),
                user=self.request.user,
            )
            user_enc.calculate_matches()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, "dispatch")
class UserEncodingDeleteView(DeleteView):
    template_name = "app/encodings/delete.html"
    model = UserEncoding
    success_url = reverse_lazy("encodings:index")


@method_decorator(staff_member_required, "dispatch")
class TestCrashView(View):
    """Test view to intentionally crash to test the error handling."""

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if not request.user.is_superuser:
            return HttpResponseForbidden("This is not for you")
        raise Exception("Test exception")
