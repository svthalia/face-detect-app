import requests
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class ConcrexitBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        auth_response = requests.post('https://thalia.nu/api/v1/token-auth/', json={
            'username': username,
            'password': password
        })
        if auth_response.ok:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(username=username)
                user.save()
            request.session['token'] = auth_response.json()['token']
            return user
        return None

    def get_user(self, user_id):
        return User.objects.filter(pk=user_id).first()

