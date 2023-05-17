from django.urls import path
from users.api.views import CustomAuthToken


urlpatterns = [
    path("api-token-auth/", CustomAuthToken.as_view()),

]
