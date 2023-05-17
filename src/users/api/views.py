from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from core.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import  exceptions
from django.contrib.auth import get_user_model
from users.models import User
from datetime import datetime, timedelta


class CustomAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username','password'],
            order=['username', 'password'],
            properties={
                'username':openapi.Schema(type=openapi.TYPE_STRING),
                'password':openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        operation_description='Get account token' 
    )
    
    def post(self, request):
        username = request.data['username']
        try:
            user = get_user_model().objects.get(email=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(('User matching query does not exist'))
        
        tokens = Token.objects.filter(user=user)
        if len(tokens)== 0:
            Token.objects.create(user=user)
        
        token = Token.objects.get(user=user)
        token = str(token)
        
        token_create_time = Token.objects.get(key=token).created
        pre_week_day = datetime.now(token_create_time.tzinfo) + timedelta(days=-7)
        if token_create_time < pre_week_day:
            Token.objects.get(key=token).delete()
            Token.objects.create(user=user)            

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        return Response({
            'username': user.email,
            'token': token
        })
