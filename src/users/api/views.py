from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import Http404, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.authentication import TokenAuthentication

User = get_user_model()

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    role = request.GET.get('role')
    qs = User.objects.all()
    if role:
        if not Group.objects.filter(name__iexact=role).exists():
            raise Http404(f"Group '{role}' does not exist.")
        qs = qs.filter(groups__name__iexact=role)
    users = []
    for user in qs:
        users.append({
            'full_name': user.get_full_name(),
            'bio': user.bio,
            'photo_url': user.get_thumbnail_url(),
            'facebook_profile_url': user.facebook_profile_url,
            'twitter_profile_url': user.twitter_profile_url,
            'github_profile_url': user.github_profile_url,
        })
    return JsonResponse(list(users), safe=False)
