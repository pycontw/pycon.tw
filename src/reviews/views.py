import collections

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404
from django.views.generic import ListView, UpdateView

from proposals.models import TalkProposal

from .apps import ReviewsConfig
from .forms import ReviewForm
from .models import REVIEW_REQUIRED_PERMISSIONS, Review


class TalkProposalListView(PermissionRequiredMixin, ListView):

    model = TalkProposal
    permission_required = REVIEW_REQUIRED_PERMISSIONS
    template_name = 'reviews/talk_proposal_list.html'
    vote_keys = {
        Review.Vote.PLUS_ONE:   'strong_accept',
        Review.Vote.PLUS_ZERO:  'weakly_accept',
        Review.Vote.MINUS_ZERO: 'weakly_reject',
        Review.Vote.MINUS_ONE:  'strong_reject',
    }
    ordering = '?'
    order_keys = {
        'title': 'title',
        'count': 'review_count',
        'category': 'category',
        'level': 'python_level',
        'lang': 'language',
        '-title': '-title',
        '-count': '-review_count',
        '-category': '-category',
        '-level': '-python_level',
        '-lang': '-language',
    }
    paginate_by = 100

    def get_ordering(self):
        params = self.request.GET
        order_key = self.order_keys.get(params.get('order', '').lower())
        if order_key:
            self.ordering = order_key
        return self.ordering

    def get_queryset(self):
        user = self.request.user
        proposals = (
            self.model.objects
            .filter(cancelled=False)
            .filter_reviewable(user)
            .exclude(review__stage=ReviewsConfig.stage, review__reviewer=user)
            .annotate(review_count=Count('review'))
        )
        # params = self.request.GET
        # category = params.get('category', '').upper()
        # if category:
        #     proposals = proposals.filter(category=category)
        return proposals.order_by(self.get_ordering())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.get_reviews()
        review_stage = ReviewsConfig.stage
        context['review_stage'] = review_stage
        context['review_stage_desc_tpl'] = (
            'reviews/_includes/review_stage_%s_desc.html'
            % review_stage
        )
        vote_count_pairs = (
            self.get_reviews()
            .values_list('vote')
            .annotate(count=Count('vote'))
        )
        context['vote'] = collections.defaultdict(
            (lambda: 0),
            ((self.vote_keys[k], v)
             for k, v in vote_count_pairs
             if k in self.vote_keys),
        )
        context['ordering'] = self.ordering
        return context

    def get_reviews(self):
        reviews = (
            self.request.user.review_set
            .filter(stage=ReviewsConfig.stage)
        )
        return reviews


class ReviewEditView(PermissionRequiredMixin, UpdateView):

    form_class = ReviewForm
    permission_required = REVIEW_REQUIRED_PERMISSIONS
    template_name = 'reviews/review_form.html'
    proposal_model = TalkProposal

    def get_proposal(self):
        try:
            proposal = (
                self.proposal_model.objects
                .filter(cancelled=False)
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

    def get_object(self):
        try:
            review = Review.objects.get(
                proposal=self.proposal,
                reviewer=self.request.user,
                stage=ReviewsConfig.stage,
            )
        except Review.DoesNotExist:
            review = None
        return review

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
