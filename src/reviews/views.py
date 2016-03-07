from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404
from django.views.generic import CreateView, ListView, UpdateView

from .apps import ReviewsConfig
from .models import Review, TalkProposal


class TalkProposalListView(PermissionRequiredMixin, ListView):

    model = TalkProposal
    permission_required = 'reviews.add_review'
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
        category = params.get('category').upper()
        if category:
            proposals = proposals.filter(category=category)
        order_key = self.order_keys.get(params.get('order').lower())
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

    model = Review
    permission_required = 'reviews.add_review'
    template_name = 'reviews/review_form.html'
    fields = ('score', 'comment', 'note', )

    def get_context_data(self, **kwargs):
        context = super(ReviewCreateView, self).get_context_data(**kwargs)
        proposal_id = self.request.GET.get('proposal_id')
        try:
            context['proposal'] = TalkProposal.objects.get(pk=proposal_id)
        except TalkProposal.DoesNotExist:
            raise Http404('Proposal not found!')

        if context['proposal'].submitter == self.request.user:
            raise PermissionDenied

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.reviewer = self.request.user
        proposal_id = self.request.GET.get('proposal_id')
        self.object.proposal = TalkProposal.objects.get(pk=proposal_id)
        return super(ReviewCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('review_proposal_list')


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):

    model = Review
    permission_required = 'reviews.add_review'
    fields = ('score', 'comment', 'note', )
    template_name = 'reviews/review_form.html'

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ReviewUpdateView, self).get_context_data(**kwargs)
        context['proposal'] = self.object.proposal
        return context

    def get_success_url(self):
        return reverse('review_proposal_list')
