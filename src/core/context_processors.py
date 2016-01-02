from django.conf import settings


def google_analytics(request):
    return {'GA_TRACK_ID': settings.GA_TRACK_ID}
