"""face_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from app import views

urlpatterns = [
    path("", views.MyPhotosView.as_view(), name="index"),
    path("token-auth/", views.TokenAuth.as_view(), name="token-auth"),
    path("admin/", admin.site.urls),
    path("user/", include("django.contrib.auth.urls")),
    path(
        "albums/",
        include(
            (
                [
                    path("", views.AlbumsIndexView.as_view(), name="index"),
                    path("<int:pk>/", views.AlbumsDetailView.as_view(), name="detail"),
                ],
                "albums",
            ),
            namespace="albums",
        ),
    ),
    path(
        "encodings/",
        include(
            (
                [
                    path("", views.UserEncodingIndexView.as_view(), name="index"),
                    path(
                        "create/", views.UserEncodingCreateView.as_view(), name="create"
                    ),
                    path(
                        "delete/<int:pk>/",
                        views.UserEncodingDeleteView.as_view(),
                        name="delete",
                    ),
                ],
                "encodings",
            ),
            namespace="encodings",
        ),
    ),
]
