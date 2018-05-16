import json
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from django.contrib.staticfiles import finders

from core.views import IndexView
from core.utils import TemplateExistanceStatusResponse
from events.models import ProposedTalkEvent
from events.views import transform_keynote_info

# Create your views here.

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
