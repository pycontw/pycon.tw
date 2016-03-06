from django.views.generic.list import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .models import TalkProposal
from .models import Review
from .forms import ReviewForm


class TalkProposalListView(PermissionRequiredMixin, ListView):
    model = TalkProposal
    permission_required = 'reviews.add_review'
    template_name = 'reviews/talkproposal_list.html'


class TalkProposalDetailView(PermissionRequiredMixin, DetailView):
    model = TalkProposal
    permission_required = 'reviews.add_review'
    template_name = 'reviews/talkproposal_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TalkProposalDetailView, self).get_context_data(**kwargs)
        review, created = Review.objects.get_or_create(
            reviewer=self.request.user, proposal=self.object
        )
        form = ReviewForm(instance=review)
        context['review'] = review
        context['form'] = form
        return context


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):
    model = Review
    permission_required = 'reviews.add_review'
    form_class = ReviewForm

    def get_success_url(self):
        return reverse('review_proposal_list')
