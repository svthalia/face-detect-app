import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class ConcrexitBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        username = username.lower() if username else username
        auth_response = requests.post(
            f"{settings.BASE_HOST}/api/v1/token-auth/",
            json={"username": username, "password": password},
        )
        if auth_response.ok:
            token = auth_response.json()["token"]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user_response = requests.post(
                    f"{settings.BASE_HOST}/api/v1/members/me",
                    headers={"Authorization": f"Token {token}"},
                ).json()
                user = User(pk=user_response["pk"], username=username)
                user.save()
            request.session["token"] = token
            return user

        return None

    def get_user(self, user_id):
        return User.objects.filter(pk=user_id).first()
