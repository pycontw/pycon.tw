from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.authentication import TokenAuthentication

ALLOWED_ROLES = {"Program", "Reviewer", "Sponsor team"}
DEFAULT_PHOTO_URL = static('images/default_head.png')


User = get_user_model()

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    role = request.GET.get('role')
    if role and role not in ALLOWED_ROLES:
        return JsonResponse({'detail': 'Invalid role.'}, status=400)
    qs = User.objects.filter(is_active=True)
    if role:
        qs = qs.filter(groups__name__iexact=role)
    users = []
    for user in qs:
        users.append({
            'full_name': user.get_full_name(),
            'bio': user.bio,
            'photo_url': '' if user.get_thumbnail_url() == DEFAULT_PHOTO_URL else user.get_thumbnail_url(),
            'facebook_profile_url': user.facebook_profile_url,
            'twitter_profile_url': user.twitter_profile_url,
            'github_profile_url': user.github_profile_url,
        })
    return JsonResponse(list(users), safe=False)
