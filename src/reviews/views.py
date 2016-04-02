import itertools
import random

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404
from django.views.generic import ListView, UpdateView

from core.utils import SequenceQuerySet
from proposals.models import TalkProposal

from .apps import ReviewsConfig
from .forms import ReviewForm
from .models import REVIEW_REQUIRED_PERMISSIONS, Review


class TalkProposalListView(PermissionRequiredMixin, ListView):

    model = TalkProposal
    permission_required = REVIEW_REQUIRED_PERMISSIONS
    template_name = 'reviews/talk_proposal_list.html'
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
        return order_key

    def get_queryset(self):
        user = self.request.user
        proposals = (
            self.model.objects
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
        if ordering:
            proposals = proposals.order_by(ordering)
            self.ordering = ordering
        else:
            proposal_list = list(proposals)
            random.shuffle(proposal_list)
            proposals = SequenceQuerySet(proposal_list)
            self.ordering = '?'
        return proposals

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review_stage = ReviewsConfig.stage

        context['reviews'] = self.get_reviews()

        verdicted_proposals = (
            TalkProposal.objects
            .filter_reviewable(self.request.user)
            .filter(accepted__isnull=False)
            .annotate(review_count=Count('review'))
        )
        context.update({
            'proposals_with_verdict': verdicted_proposals,
        })

        context['review_stage'] = review_stage
        context['review_stage_desc_tpl'] = (
            'reviews/_includes/review_stage_%s_desc.html'
            % review_stage
        )

        context['vote'] = {
            'strong_accept': context['reviews'].filter(
                vote=Review.Vote.PLUS_ONE).count(),
            'weak_accept': context['reviews'].filter(
                vote=Review.Vote.PLUS_ZERO).count(),
            'weak_reject': context['reviews'].filter(
                vote=Review.Vote.MINUS_ZERO).count(),
            'strong_reject': context['reviews'].filter(
                vote=Review.Vote.MINUS_ONE).count(),
        }
        context['ordering'] = self.ordering
        context['query_string'] = self.request.GET.urlencode()
        return context

    def get_reviews(self):
        review_stage = ReviewsConfig.stage
        if review_stage == 1:
            reviews = (
                Review.objects
                .filter_reviewable(self.request.user)
                .exclude(stage=2)
            )
        elif review_stage == 2:
            proposals = TalkProposal.objects.filter(
                    review__stage=1,
                    review__reviewer=self.request.user
                ) & TalkProposal.objects.filter(
                    review__stage=2,
                    review__reviewer=self.request.user
                )
            reviews = (
                Review.objects
                .filter_reviewable(self.request.user)
                .filter(proposal__accepted__isnull=True)
                .exclude(proposal__in=proposals, stage=1)
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
        review_stage = ReviewsConfig.stage
        # Query all reviews made by others, including all stages
        full_other_reviews = (
            Review.objects
            .filter_current_reviews(
                proposal=self.proposal,
                exclude_user=self.request.user,
            )
            .order_by('vote', '-stage')
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
