from django.views.generic.list import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import UpdateView, CreateView
from django.core.urlresolvers import reverse
from django.http import Http404

from .models import TalkProposal
from .models import Review
from .forms import ReviewForm


class TalkProposalListView(PermissionRequiredMixin, ListView):
    model = TalkProposal
    permission_required = 'reviews.add_review'
    template_name = 'reviews/talkproposal_list.html'

    def get_queryset(self):
        return TalkProposal.objects.exclude(
            review__reviewer=self.request.user,
        ).exclude(
            submitter=self.request.user
        )

class ReviewCreateView(PermissionRequiredMixin, CreateView):
    model = Review
    permission_required = 'reviews.add_review'
    template_name = 'reviews/review_form.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super(ReviewCreateView, self).get_context_data(**kwargs)
        proposal_id = self.request.GET.get('proposal_id')
        try:
            context['proposal'] = TalkProposal.objects.get(pk=proposal_id)
        except TalkProposal.DoesNotExist:
            raise Http404('Proposal not found!')
        context['form'] = ReviewForm(
            initial={
                'reviewer': self.request.user,
                'proposal': context['proposal'],
            }
        )

        return context

    def get_success_url(self):
        return reverse('review_proposal_list')


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):
    model = Review
    permission_required = 'reviews.add_review'
    fields = ('score', 'comment', 'note', )
    template_name = 'reviews/review_form.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewUpdateView, self).get_context_data(**kwargs)
        context['proposal'] = self.object.proposal
        return context

    def get_success_url(self):
        return reverse('review_proposal_list')
