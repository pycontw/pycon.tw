import collections
import json
import random

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.db.models import Count
from django.http import Http404
from django.views.generic import ListView, UpdateView

from core.utils import SequenceQuerySet
from proposals.models import TalkProposal

from .forms import ReviewForm
from .models import REVIEW_REQUIRED_PERMISSIONS, Review, TalkProposalSnapshot
from .context import reviews_state


class ReviewableMixin:
    def dispatch(self, request, *args, **kwargs):
        self.reviews_state = reviews_state()

        if self.reviews_state.reviews_stage < 1:
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
        'count': 'review__count',
        'category': 'category',
        'level': 'python_level',
        'lang': 'language',
        '-title': '-title',
        '-count': '-review__count',
        '-category': '-category',
        '-level': '-python_level',
        '-lang': '-language',
    }
    paginate_by = 150

    def get_ordering(self):
        params = self.request.GET
        order_key = self.order_keys.get(params.get('order', '').lower())
        return order_key or '?'

    def get_category(self):
        params = self.request.GET
        return params.get('category')

    def get_queryset(self):
        user = self.request.user
        qs = (
            super().get_queryset()
            .filter_reviewable(user)
            .exclude(accepted__isnull=False)
            .exclude(review__reviewer=user)
            .annotate(Count('review'))
        )

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
        self.category = self.get_category()

        return qs

    def get_category_metrics(self, context):
        count = 0
        categories = set()
        for proposal in context["object_list"]:
            if proposal.category == self.category:
                count += 1
            if proposal.category not in categories:
                categories.add(proposal.category)
        return {
            "category_options": categories,
            "filtered_count": count if count else len(context["object_list"])
        }

    def get_context_data(self, **kwargs):
        review_stage = self.reviews_state.reviews_stage
        verdicted_proposals = (
            TalkProposal.objects
            .filter_reviewable(self.request.user)
            .filter(accepted__isnull=False)
            .annotate(Count('review'))
        )

        stage_1_vote_count_pairs = (
            self.get_stage_1_reviews()
            # This transform is needed to clear the default ordering in
            # the model. The default ordering contributes to GROUP BY, and
            # breaks the COUNT aggregation.
            .order_by()
            .values_list('vote')
            .annotate(count=Count('vote'))
        )
        stage_2_vote_count_pairs = (
            self.get_stage_2_reviews()
            # This transform is needed to clear the default ordering in
            # the model. The default ordering contributes to GROUP BY, and
            # breaks the COUNT aggregation.
            .order_by()
            .values_list('vote')
            .annotate(count=Count('vote'))
        )
        vote_count_pairs = stage_1_vote_count_pairs.union(stage_2_vote_count_pairs, all=True)
        vote_mapping = collections.defaultdict(int)
        for k, v in vote_count_pairs:
            vote_mapping[self.vote_keys[k]] += v

        context = super().get_context_data(**kwargs)
        context.update({
            'proposals_with_verdict': verdicted_proposals,
            'stage_1_reviews': self.get_stage_1_reviews(),
            'stage_2_reviews': self.get_stage_2_reviews(),
            'total_reviewed_amount': len(self.get_stage_1_reviews()) + len(self.get_stage_2_reviews()),
            'review_stage': review_stage,
            'review_stage_desc_tpl': (
                'reviews/_includes/review_stage_%s_desc.html'
                % review_stage
            ),
            'vote': vote_mapping,
            'ordering': self.ordering,
            'category': self.category,
            'query_string': self.request.GET.urlencode(),
            **self.reviews_state._asdict(),
            **self.get_category_metrics(context),
        })
        return context

    def get_stage_1_reviews(self):
        review_stage = self.reviews_state.reviews_stage
        if review_stage == 1:
            stage_1_reviews = (
                Review.objects
                .select_related('proposal')
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
            stage_1_reviews = (
                Review.objects
                .select_related('proposal')
                .filter_reviewable(self.request.user)
                .filter(proposal__accepted__isnull=True)
                .exclude(proposal__in=proposals, stage=1)
                .exclude(stage=2)
            )
        return stage_1_reviews

    def get_stage_2_reviews(self):
        review_stage = self.reviews_state.reviews_stage
        if review_stage == 1:
            return Review.objects.none()
        elif review_stage == 2:
            stage_2_reviews = (
                Review.objects
                .select_related('proposal')
                .filter_reviewable(self.request.user)
                .filter(proposal__accepted__isnull=True)
                .exclude(stage=1)
            )
        return stage_2_reviews


class ReviewEditView(ReviewableMixin, PermissionRequiredMixin, UpdateView):

    form_class = ReviewForm
    permission_required = REVIEW_REQUIRED_PERMISSIONS
    template_name = 'reviews/review_form.html'
    proposal_model = TalkProposal
    snapshot_model = TalkProposalSnapshot

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

    def get_snapshot(self, proposal):
        try:
            snapshot = (
                self.snapshot_model.objects
                .filter(
                    proposal=proposal,
                    stage__lt=self.reviews_state.reviews_stage
                )
                .latest('dumped_at')
            )
        except self.snapshot_model.DoesNotExist:
            return None
        try:
            snapshot = TalkProposal(**json.loads(snapshot.dumped_json))
        except (TypeError, ValueError):
            return None
        return snapshot

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
                stage=self.reviews_state.reviews_stage,
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
        if kwargs.get('instance') is not None or kwargs.get('initial'):
            return kwargs
        try:
            review = Review.objects.get(
                proposal=self.proposal,
                reviewer=self.request.user,
                stage=self.reviews_state.reviews_stage - 1,
            )
        except Review.DoesNotExist:
            return kwargs
        kwargs['initial'] = {
            'vote': review.vote,
            'comment': review.comment,
            'note': review.note,
            'discloses_comment': review.discloses_comment,
        }
        return kwargs

    def get_context_data(self, **kwargs):
        review_stage = self.reviews_state.reviews_stage
        # Query all reviews made by others, including all stages
        other_review_iter = (
            Review.objects
            .filter_current_reviews(
                proposal=self.proposal,
                exclude_user=self.request.user,
            )
            .iter_reviewer_latest_reviews()
        )
        # Sort other_reviews by vote.
        other_reviews = sorted(
            other_review_iter,
            key=lambda r: Review.VOTE_ORDER[r.vote],
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
            'snapshot': self.get_snapshot(self.proposal),
            'other_reviews': other_reviews,
            'my_reviews': my_reviews,
            'review_stage': review_stage,
            **self.reviews_state._asdict(),
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        query_string = self.request.GET.urlencode()
        url = reverse('review_proposal_list')
        if query_string:
            return url + '?' + query_string
        return url
