import collections
import json
import operator

from django.contrib import admin
from django.utils.html import linebreaks
from django.utils.translation import ugettext, gettext_lazy as _

from import_export.admin import ImportExportMixin

from .models import Review, TalkProposalSnapshot
from .resources import ReviewResource


@admin.register(Review)
class ReviewAdmin(ImportExportMixin, admin.ModelAdmin):
    fields = [
        'reviewer', 'stage', 'proposal', 'vote', 'comment', 'note',
        'discloses_comment', 'appropriateness', 'updated',
    ]
    readonly_fields = ['updated']
    list_display = [
        'proposal', 'vote', 'reviewer',
        'stage', 'discloses_comment', 'appropriateness',
    ]
    list_filter = [
        'vote', 'stage', 'discloses_comment', 'appropriateness',
    ]
    search_fields = ['proposal__title']
    resource_class = ReviewResource


@admin.register(TalkProposalSnapshot)
class TalkProposalSnapshotAdmin(admin.ModelAdmin):

    fields = ['proposal', 'stage', 'get_dumped_data_display', 'dumped_at']
    list_display = ['proposal', 'stage', 'dumped_at']
    readonly_fields = fields

    def get_dumped_data_display(self, instance):

        def make_object(pairs):
            pairs = sorted(pairs, key=operator.itemgetter(0))
            return collections.OrderedDict(pairs)

        dumped_data = json.loads(
            instance.dumped_json, object_pairs_hook=make_object,
        )
        parts = [
            '<table><thead><tr><th>',
            ugettext('Key'),
            '</th><th>',
            ugettext('Value'),
            '</th></tr></thead><tbody>',
        ]
        for key, value in dumped_data.items():
            parts.extend([
                '<tr><th>',
                key,
                '</th><td>',
                linebreaks(value),
                '</td></tr>',
            ])
        parts.append('</tbody></table>')
        return ''.join(parts)

    get_dumped_data_display.allow_tags = True
    get_dumped_data_display.short_description = _('dumped data')
