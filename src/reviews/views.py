import collections
import itertools
import random

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404
from django.views.generic import ListView, UpdateView

from core.utils import SequenceQuerySet
from proposals.models import TalkProposal

from .forms import ReviewForm
from .models import REVIEW_REQUIRED_PERMISSIONS, Review


class ReviewableMixin:
    def dispatch(self, request, *args, **kwargs):
        if settings.REVIEWS_STAGE < 1:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class TalkProposalListView(ReviewableMixin, PermissionRequiredMixin, ListView):

    model = TalkProposal
    permission_required = REVIEW_REQUIRED_PERMISSIONS
    template_name = 'reviews/talk_proposal_list.html'
    vote_keys = {
        Review.Vote.PLUS_ONE: 'strong_accept',
        Review.Vote.PLUS_ZERO: 'weak_accept',
        Review.Vote.MINUS_ZERO: 'weak_reject',
        Review.Vote.MINUS_ONE: 'strong_reject',
    }
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
        return order_key or '?'

    def get_queryset(self):
        user = self.request.user
        qs = (
            super().get_queryset()
            .filter_reviewable(user)
            .exclude(accepted__isnull=False)
            .exclude(review__reviewer=user)
            .annotate(review_count=Count('review'))
        )
        # params = self.request.GET
        # category = params.get('category', '').upper()
        # if category:
        #     proposals = proposals.filter(category=category)
        ordering = self.get_ordering()
        if ordering == '?':
            # We don't use order_by('?') because it is crazy slow, and instead
            # resolve the queryset to a list, and shuffle it normally. This is
            # OK since we will iterate through it in the template anyway.

            # Note: This order by is necessary to override the default
            # ordering, and add an appropriate DISTINCT on the query. This
            # is caused by a Django logic error regarding how ORDER BY
            # contributes to GROUP BY.
            proposal_list = list(qs.order_by('pk'))
            random.shuffle(proposal_list)
            qs = SequenceQuerySet(proposal_list)
            ordering = '?'
        else:
            qs = qs.order_by(ordering)
        self.ordering = ordering
        return qs

    def get_context_data(self, **kwargs):
        review_stage = settings.REVIEWS_STAGE
        verdicted_proposals = (
            TalkProposal.objects
            .filter_reviewable(self.request.user)
            .filter(accepted__isnull=False)
            .annotate(review_count=Count('review'))
        )

        vote_count_pairs = (
            self.get_reviews()
            # This transform is needed to clear the default ordering in
            # the model. The default ordering contributes to GROUP BY, and
            # breaks the COUNT aggregation.
            .order_by()
            .values_list('vote')
            .annotate(count=Count('vote'))
        )
        vote_mapping = collections.defaultdict(
            (lambda: 0),
            ((self.vote_keys[k], v)
             for k, v in vote_count_pairs
             if k in self.vote_keys),
        )

        context = super().get_context_data(**kwargs)
        context.update({
            'proposals_with_verdict': verdicted_proposals,
            'reviews': self.get_reviews(),
            'review_stage': review_stage,
            'review_stage_desc_tpl': (
                'reviews/_includes/review_stage_%s_desc.html'
                % review_stage
            ),
            'vote': vote_mapping,
            'ordering': self.ordering,
            'query_string': self.request.GET.urlencode(),
        })
        return context

    def get_reviews(self):
        review_stage = settings.REVIEWS_STAGE
        if review_stage == 1:
            reviews = (
                Review.objects
                .filter_reviewable(self.request.user)
                .exclude(stage=2)
            )
        elif review_stage == 2:
            proposals = (
                TalkProposal.objects.filter(
                    review__stage=1,
                    review__reviewer=self.request.user
                ) & TalkProposal.objects.filter(
                    review__stage=2,
                    review__reviewer=self.request.user
                )
            )
            reviews = (
                Review.objects
                .filter_reviewable(self.request.user)
                .filter(proposal__accepted__isnull=True)
                .exclude(proposal__in=proposals, stage=1)
            )
        return reviews


class ReviewEditView(ReviewableMixin, PermissionRequiredMixin, UpdateView):

    form_class = ReviewForm
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
        if self.proposal.accepted is not None:
            return self.http_method_not_allowed(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def get_object(self):
        try:
            review = Review.objects.get(
                proposal=self.proposal,
                reviewer=self.request.user,
                stage=settings.REVIEWS_STAGE,
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
        review_stage = settings.REVIEWS_STAGE
        # Query all reviews made by others, including all stages
        full_other_reviews = (
            Review.objects
            .filter_current_reviews(
                proposal=self.proposal,
                exclude_user=self.request.user,
            )
            .order_by('reviewer', '-stage')
        )
        # Select only the latest stage review for each reviewer
        # by first grouping reviews based on reviewer.
        # Note that this requires the QuerySet already sorted by reviewer
        grouped_reviews_per_reviewers = itertools.groupby(
            full_other_reviews, key=lambda r: r.reviewer
        )
        other_reviews = (
            # we sorted the reviews by descending stage
            next(reviews_by_same_reviewer)
            for _, reviews_by_same_reviewer in grouped_reviews_per_reviewers
        )
        # Sort other_reviews by vote
        VOTE_ORDER = {'+1': 3, '+0': 2, '-0': 1, '-1': 0}
        other_reviews = sorted(
            other_reviews,
            key=lambda r: VOTE_ORDER[r.vote],
            reverse=True,
        )
        my_reviews = (
            Review.objects
            .filter_current_reviews(
                proposal=self.proposal,
                filter_user=self.request.user,
            )
            .order_by('stage')
        )
        if self.proposal.accepted is None and self.object:
            # If this proposal does not have verdict, this page will have a
            # review form. Exclude the current user's current review so that
            # it does not show up twice (once in the table, once in form).
            my_reviews = my_reviews.exclude(pk=self.object.pk)

        kwargs.update({
            'proposal': self.proposal,
            'other_reviews': other_reviews,
            'my_reviews': my_reviews,
            'review_stage': review_stage,
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        query_string = self.request.GET.urlencode()
        url = reverse('review_proposal_list')
        if query_string:
            return url + '?' + query_string
        return url
