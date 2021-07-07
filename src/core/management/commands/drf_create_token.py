from django.contrib.auth import get_user_model
from rest_framework.authtoken.management.commands.drf_create_token import Command

from core.models import Token

UserModel = get_user_model()


class Command(Command):
    def create_user_token(self, username, reset_token):
        user = UserModel._default_manager.get_by_natural_key(username)

        if reset_token:
            Token.objects.filter(user=user).delete()

        token = Token.objects.get_or_create(user=user)
        return token[0]
