from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings

from collections import OrderedDict
import re

from registry.helper import reg

from .models import Attendee


token_re = re.compile(r'^[0-9a-f]{32}$')


def live(request):
    token = request.GET.get('token', '')

    if not token_re.match(token):
        raise Http404

    attendee = None

    try:
        attendee = Attendee.objects.get(token=token)
    except Attendee.DoesNotExist:
        attendee = Attendee.objects.create(token=token)

    rooms = OrderedDict()
    rooms['R0'] = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r0', '')
    rooms['R1'] = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r1', '')
    rooms['R2'] = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r2', '')

    return render(request, 'ext/live.html', {
        'attendee': attendee,
        'rooms': rooms,
        'token': token,
    })

def discord(request):
    token = request.GET.get('token', '')
    return render(request, 'ext/discord.html', {'token': token})
