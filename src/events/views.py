import collections

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, TemplateView

from core.mixins import FormValidMessageMixin
from proposals.models import TalkProposal

from .forms import ScheduleCreationForm
from .models import Schedule, SponsoredEvent
from .renderers import render_all


class AcceptedTalkMixin:
    queryset = (
        TalkProposal.objects
        .filter_accepted()
        .select_related('submitter')
    )


class TalkListView(AcceptedTalkMixin, TemplateView):

    template_name = 'events/talk_list.html'

    def get_categorized_talks(self):
        category_map = collections.defaultdict(list)
        for proposal in self.queryset:
            category_map[proposal.get_category_display()].append(proposal)
        return category_map

    def get_sponsored_talks(self):
        sponsored_events = (
            SponsoredEvent.objects
            .select_related('host')
            .order_by('title')
        )
        return sponsored_events

    def get_context_data(self, **kwargs):
        kwargs.update({
            'talk_category_list_pairs': self.get_categorized_talks().items(),
            'sponsored_events': self.get_sponsored_talks(),
        })
        return super().get_context_data(**kwargs)


class ScheduleView(TemplateView):

    template_name = 'events/schedule.html'

    def get(self, request, *args, **kwargs):
        try:
            self.schedule = Schedule.objects.latest()
        except Schedule.DoesNotExist:
            return HttpResponseRedirect(
                'https://docs.google.com/spreadsheets/d/'
                '17-8E1OhfgiG4pIOIrp3OpNY4OaK1QxUn4TJK9oVmRSw/htmlview',
            )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            schedule_html=self.schedule.html,
            **kwargs
        )


class ScheduleCreateView(
        FormValidMessageMixin, PermissionRequiredMixin, CreateView):

    form_class = ScheduleCreationForm
    form_valid_message = _('New talk schedule generated successfully.')
    permission_required = ['events.add_schedule']
    template_name = 'events/schedule_create.html'

    def get_success_url(self):
        return reverse('events_schedule')

    def get_context_data(self, **kwargs):
        return super().get_context_data(content=render_all(), **kwargs)


class TalkDetailView(AcceptedTalkMixin, DetailView):
    template_name = 'events/talk_detail.html'


class SponsoredEventDetailView(DetailView):

    model = SponsoredEvent
    template_name = 'events/sponsored_event_detail.html'

    def get_queryset(self):
        """Fetch user relation before-hand because we'll need it.
        """
        return super().get_queryset().select_related('host')
