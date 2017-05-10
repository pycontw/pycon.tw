import collections
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.template import Library
from django.utils.html import linebreaks

from sponsors.models import Sponsor


register = Library()


@register.filter
def sponsor_jsonize(sponsors):
    sponsor_lists = {level: [] for level, _ in Sponsor.LEVEL_CHOICES}
    sponsor_info_dict = collections.OrderedDict(
        ('level-{}'.format(level), {
            'name': name,
            'sponsors': sponsor_lists[level],
        })
        for (level, name) in Sponsor.LEVEL_CHOICES
    )
    for sponsor in sponsors:
        sponsor_info = {
            'name': sponsor.name,
            'website_url': sponsor.website_url,
            'intro_html': linebreaks(sponsor.intro),
        }
        if sponsor.logo:
            sponsor_info['logo'] = sponsor.logo.url
        sponsor_lists[sponsor.level].append(sponsor_info)
    return json.dumps({'sponsors': sponsor_info_dict}, cls=DjangoJSONEncoder)
