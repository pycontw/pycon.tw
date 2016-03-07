from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404
from django.views.generic import CreateView, ListView, UpdateView

from proposals.models import TalkProposal

from .apps import ReviewsConfig
from .forms import ReviewCreateForm
from .models import REVIEW_REQUIRED_PERMISSIONS, Review


class TalkProposalListView(PermissionRequiredMixin, ListView):

    model = TalkProposal
    permission_required = REVIEW_REQUIRED_PERMISSIONS
    template_name = 'reviews/talk_proposal_list.html'
    order_keys = {
        'title': 'title',
        'reviews': 'review_count',
    }

    def get_queryset(self):
        params = self.request.GET
        user = self.request.user
        proposals = (
            self.model.objects
            .filter_reviewable(user)
            .exclude(review__stage=ReviewsConfig.stage, review__reviewer=user)
            .annotate(review_count=Count('review'))
        )
        category = params.get('category', '').upper()
        if category:
            proposals = proposals.filter(category=category)
        order_key = self.order_keys.get(params.get('order', '').lower())
        return proposals.order_by(order_key or '?')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.get_reviews()
        return context

    def get_reviews(self):
        reviews = (
            self.request.user.review_set
            .filter(stage=ReviewsConfig.stage)
        )
        return reviews


class ReviewCreateView(PermissionRequiredMixin, CreateView):

    form_class = ReviewCreateForm
    permission_required = REVIEW_REQUIRED_PERMISSIONS
    template_name = 'reviews/review_form.html'
    proposal_model = TalkProposal

    def get_proposal(self):
        try:
            proposal = (
                self.proposal_model.objects
                .filter_reviewable(self.request.user)
                .get(pk=self.kwargs['proposal_pk'])
            )
        except self.proposal_model.DoesNotExist:
            raise Http404
        return proposal

    def get(self, request, *args, **kwargs):
        self.proposal = self.get_proposal()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.proposal = self.get_proposal()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'proposal': self.proposal,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['proposal'] = self.proposal
        return data

    def get_success_url(self):
        return reverse('review_proposal_list')


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):

    model = Review
    fields = ['score', 'comment', 'note']
    permission_required = REVIEW_REQUIRED_PERMISSIONS
    template_name = 'reviews/review_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(reviewer=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['proposal'] = self.object.proposal
        return data

    def get_success_url(self):
        return reverse('review_proposal_list')
