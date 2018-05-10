from proposals.models import TalkProposal
from events.models import KeynoteEvent, ProposedTalkEvent, CustomEvent
# from django.core import serializers
from django.http import JsonResponse
import datetime as dt
import pytz


def get_ccip_events_json(request):
    import pprint
    pprint.pprint(list(ProposedTalkEvent.objects.values())[0])
    proposed_talk_events = ProposedTalkEvent.objects.select_related('proposal__submitter')

    json_data_list = list()
    for event in proposed_talk_events:
        json_dict = dict()
        json_dict['speaker'] = dict()
        json_dict['speaker']['bio'] = event.proposal.submitter.bio
        json_dict['speaker']['name'] = event.proposal.submitter.speaker_name
        json_dict['speaker']['avatar'] = event.proposal.submitter.get_photo_url()
        # json_dict['speaker']['avatar'] = request.build_absolute_uri(event.proposal.submitter.photo.url)
        json_dict['subject'] = event.proposal.title
        json_dict['summary'] = event.proposal.abstract
        json_dict['type'] = ''
        json_dict['room'] = event.location[-2:].upper()
        json_dict['start'] = event.begin_time.value.isoformat()
        json_dict['end'] = event.end_time.value.isoformat()
        json_dict['id'] = event.proposal.id
        json_data_list.append(json_dict)
        print(json_dict)

    # Keynote #1
    json_dict = dict()
    json_dict['speaker'] = dict()
    json_dict['speaker']['bio'] = ''
    json_dict['speaker']['name'] = '陳昇瑋'
    json_dict['speaker']['avatar'] = 'https://tw.pycon.org/2018/static/images/default_head.png'
    # json_dict['speaker']['avatar'] = request.build_absolute_uri(event.proposal.submitter.photo.url)
    json_dict['subject'] = ''
    json_dict['summary'] = ''
    json_dict['type'] = ''
    json_dict['room'] = 'R0'
    json_dict['start'] = dt.datetime(2018, 6, 1, 9, 20, 0, tzinfo=pytz.FixedOffset(8*60)).isoformat()
    json_dict['end'] = dt.datetime(2018, 6, 1, 10, 20, 0, tzinfo=pytz.FixedOffset(8*60)).isoformat()
    json_dict['id'] = 1
    json_data_list.append(json_dict)

    # Keynote #2
    json_dict = dict()
    json_dict['speaker'] = dict()
    json_dict['speaker']['bio'] = """
Katie has worn many different hats over the years. She has been a software developer for many languages, systems administrator for multiple operating systems, and speaker on many different topics. 

When she’s not changing the world, she enjoys making tapestries, cooking, and seeing just how well various application stacks handle emoji.
    """
    json_dict['speaker']['name'] = 'Katie McLaughlin'
    json_dict['speaker']['avatar'] = 'https://tw.pycon.org/2018/static/pycontw-2018/assets/keynotes/katie.jpg'
    # json_dict['speaker']['avatar'] = request.build_absolute_uri(event.proposal.submitter.photo.url)
    json_dict['subject'] = 'Communication strategies beyond the Basic Multilingual Plane'
    json_dict['summary'] = """
The standardisation of the universal character set has paved the way for the ability for data to be freely transferred between computers around the world. However, the most volatile part of this standard is still causing prolific issues with miscommunication between humans.

In this keynote, Katie McLaughlin will share knowledge from her years of research and contributions to this field and rant about emoji for a bit.
    """
    json_dict['type'] = ''
    json_dict['room'] = 'R0'
    json_dict['start'] = dt.datetime(2018, 6, 1, 9, 10, 0, tzinfo=pytz.FixedOffset(8*60)).isoformat()
    json_dict['end'] = dt.datetime(2018, 6, 1, 10, 10, 0, tzinfo=pytz.FixedOffset(8*60)).isoformat()
    json_dict['id'] = 2
    json_data_list.append(json_dict)

    # pprint.pprint(json_dict)
    return JsonResponse(json_data_list, safe=False)
