from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from collections import OrderedDict
import re

from registry.helper import reg

from core.utils import collect_language_codes
from django.core.exceptions import ImproperlyConfigured
from .models import Attendee,Venue, Choice
import datetime
from .forms import CommunityTrackForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView

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
    rooms['R1'] = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r1', '')
    rooms['R2'] = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r2', '')
    rooms['R3'] = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r3', '')

    return render(request, 'ext/live.html', {
        'attendee': attendee,
        'rooms': rooms,
        'token': token,
    })


class CommunityTrackView(ListView):
    model = Venue
    template_name = 'events/community_track.html'

    def dispatch(self, request, *args, **kwargs):
        self.attendee = None
        self.choice = None
        self.message = None
        self.token = request.GET.get('token')

        # Get attendee
        if self.token:
            try:
                self.attendee = Attendee.objects.get(token=self.token)
            except Attendee.DoesNotExist:
                # Should we build one here (?)
                self.message = _("The token within the link is invalid. Please contact the administrator for further help.")
            except Attendee.MultipleObjectsReturned:
                # Should never happen
                pass
        else:
            self.message = _("You can choose the track you'd like to go if you access this page from the preparation letter, " \
                             "or from the OPass app that is already bound with your KKTIX registration.")

        if self.attendee:
            # Get the choice
            try:
                self.choice = Choice.objects.get(attendee=self.attendee)
            except Choice.DoesNotExist:
                pass
            except Choice.MultipleObjectsReturned:
                # Should never happen... what to do?
                # Get the latest and delete all others
                self.choice = Choice.objects.filter(attendee=self.attendee).order_by('-selected_time').first()
                Choice.objects.exclude(pk=self.choice.pk).delete()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        forms_obj = CommunityTrackForm(request.POST, instance=self.choice)

        if forms_obj.is_valid():
            forms_obj.save()
            return HttpResponseRedirect(self.request.get_full_path())

    def get_context_data(self, **kwargs):
        kwargs.update({
            'selected_venue': self.choice.venue if self.choice else None,
            'attendee': self.attendee,
            'message': self.message,
            'token': self.token,
        })
        return super().get_context_data(**kwargs)
