import json

from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.generic import View, TemplateView

from core.views import IndexView
from core.utils import TemplateExistanceStatusResponse
from events.models import ProposedTalkEvent


def convert_to_utc(value):
    # CCIP on Android does not take offset well because Java's timezone API
    # sucks. Convert to UTC because we ought to help those poor souls.
    return timezone.make_aware(parse_datetime(value)).astimezone(timezone.utc)


def transform_keynote_info(request, i, info):
    info['id'] = f'keynote-{i}'
    info['type'] = ''   # Not used.
    info['start'] = convert_to_utc(info['start'])
    info['end'] = convert_to_utc(info['end'])
    info['speaker']['avatar'] = request.build_absolute_uri(
        static(info['speaker']['avatar']),
    )
    return info


class CCIPAPIView(View):
    def get(self, request):
        dataset = [
            {
                'id': f'talk-{event.pk}',
                'subject': event.proposal.title,
                'summary': event.proposal.abstract,
                'type': '',     # Not used.
                'room': event.get_location_display(),
                'start': event.begin_time.value.isoformat(),
                'end': event.end_time.value.isoformat(),
                'speaker': {
                    'name': event.proposal.submitter.speaker_name,
                    'avatar': request.build_absolute_uri(
                        event.proposal.submitter.get_photo_url(),
                    ),
                    'bio': event.proposal.submitter.bio,
                },
            }
            for event in ProposedTalkEvent.objects.select_related(
                'proposal', 'proposal__submitter',
            )
        ]
        with open(finders.find('pycontw-2018/assets/keynotes/info.json')) as f:
            dataset.extend(
                transform_keynote_info(request, i, info)
                for i, info in enumerate(json.load(f), 1)
            )
        return JsonResponse(dataset, safe=False)


class CCIPSponsorsView(IndexView):
    template_name = 'ccip/sponsors.html'
    response_class = TemplateExistanceStatusResponse


class CCIPStaffView(TemplateView):
    template_name = 'ccip/staff.html'
    response_class = TemplateExistanceStatusResponse
