from django.conf import settings
from django.urls import get_script_prefix


def _build_google_form_url(uid):
    return f'https://docs.google.com/forms/d/e/{uid}/viewform'


def script_prefix(request):
    return {
        'SCRIPT_PREFIX': get_script_prefix(),
    }


def pycontw(request):
    volun_id = '1FAIpQLScYhMAg4_T4Shi-W0vt9EkGyrpTMHemvcY55ZKc2-MfVqDzGg'
    return {
        'GTM_TRACK_ID': settings.GTM_TRACK_ID,
        'KKTIX_URL': {
            'RSVD': 'https://pycontw.kktix.cc/events/20200905-reserved',
            'INDI': 'https://pycontw.kktix.cc/events/20200905-individual',
            'CORP': 'https://pycontw.kktix.cc/events/20200905-corporate',
        },
        'VOLUNTEER_FORM_URL': _build_google_form_url(volun_id),
    }


def frontend_host(request):
    return {'FRONTEND_HOST': settings.FRONTEND_HOST}
