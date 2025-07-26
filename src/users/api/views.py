from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.authentication import TokenAuthentication

User = get_user_model()


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    role = request.GET.get('role')
    if not role or role != "Reviewer":
        return JsonResponse({'detail': 'role is not given or invalid.'}, status=400)
    qs = User.objects.get_valid_users_by_role(role).order_by('speaker_name')
    users = []
    for user in qs:
        users.append({
            'full_name': user.get_full_name(),
            'bio': user.bio,
            'photo_url': user.get_thumbnail_url(default_value=None),
            'facebook_profile_url': user.facebook_profile_url,
            'twitter_profile_url': user.twitter_profile_url,
            'github_profile_url': user.github_profile_url,
        })
    return JsonResponse(list(users), safe=False)
