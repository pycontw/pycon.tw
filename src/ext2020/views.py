from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings

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
    rooms['R0'] = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r0', '')
    rooms['R1'] = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r1', '')
    rooms['R2'] = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r2', '')

    return render(request, 'ext/live.html', {
        'attendee': attendee,
        'rooms': rooms,
        'token': token,
    })




class CommunityTrackView(ListView):
    model = Venue
    path = 'events/community-track'
    success_url = reverse_lazy('community-track')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        data = request.POST.copy()
        data['selected_time'] = datetime.datetime.now()
        forms_obj = CommunityTrackForm(data)
        if forms_obj.is_valid():
            Choice.objects.create(**forms_obj.cleaned_data)
            return HttpResponseRedirect(self.get_success_url())




    def get_context_data(self, **kwargs):
        token = self.request.GET.get('token')
        venue_choice = Venue.objects.filter(choice__attendee_token=token)
        kwargs.update({
            'venue_choice': venue_choice.first() if venue_choice else '',
            'token': token,
        })
        return super().get_context_data(**kwargs)

    def get_template_names(self):
        template_names = [
            '/'.join(['contents', code, self.path + '.html'])
            for code in collect_language_codes(self.request.LANGUAGE_CODE)
        ]
        # print(template_names)
        return template_names

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy

