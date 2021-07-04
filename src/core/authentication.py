from rest_framework.authentication import TokenAuthentication
from .models import Token


class TokenAuthentication(TokenAuthentication):
    model = Token
