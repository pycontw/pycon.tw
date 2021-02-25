import itertools
import operator

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext, gettext_lazy as _

from registry.helper import reg

from core.models import BigForeignKey, DefaultConferenceManager
from proposals.models import TalkProposal


REVIEW_REQUIRED_PERMISSIONS = ['reviews.add_review']


class ReviewQuerySet(models.QuerySet):

    def filter_current_reviews(
            self, proposal, exclude_user=None, filter_user=None):
        qs = self.filter(proposal=proposal)
        stage = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.reviews.stage', 0)
        if stage:
            qs = qs.filter(stage__lte=stage)
        if exclude_user:
            qs = qs.exclude(reviewer=exclude_user)
        if filter_user:
            qs = qs.filter(reviewer=filter_user)
        return qs

    def filter_reviewable(self, user):
        cospeaking = user.cospeaking_info_set.all()
        qs = self.exclude(
            Q(proposal__cancelled=True) |
            Q(proposal__submitter=user) |
            Q(proposal__additionalspeaker_set__in=cospeaking)
        )
        qs = qs.filter(reviewer=user)
        return qs

    def iter_reviewer_latest_reviews(self):
        review_qs = self.order_by('reviewer', '-stage')
        # Select only the latest stage review for each reviewer
        # by first grouping reviews based on reviewer.
        # Note that this requires the QuerySet already sorted by reviewer.
        grouped_per_reviewer_reviews = itertools.groupby(
            review_qs, key=operator.attrgetter('reviewer')
        )
        # Since we sorted the reviews by descending stage, next() will return
        # the latest review by each reviewer.
        return [
            next(reviews_by_same_reviewer)
            for _, reviews_by_same_reviewer in grouped_per_reviewer_reviews
        ]


class ReviewManager(DefaultConferenceManager.from_queryset(ReviewQuerySet)):
    conference_attr = 'proposal__conference'


class Review(models.Model):

    reviewer = BigForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_('reviewer'),
        on_delete=models.CASCADE,
    )

    stage = models.IntegerField(
        verbose_name=_('stage'),
    )

    proposal = models.ForeignKey(
        to=TalkProposal,
        verbose_name=_('proposal'),
        on_delete=models.CASCADE,
    )

    objects = ReviewManager()
    all_objects = ReviewQuerySet.as_manager()

    class Vote:
        PLUS_ONE = '+1'
        PLUS_ZERO = '+0'
        MINUS_ZERO = '-0'
        MINUS_ONE = '-1'

    VOTE_CHOICES = (
        (Vote.PLUS_ONE, _('+1 (strong accept)')),
        (Vote.PLUS_ZERO, _('+0 (weak accept)')),
        (Vote.MINUS_ZERO, _('-0 (weak reject)')),
        (Vote.MINUS_ONE, _('-1 (strong reject)')),
    )

    VOTE_ORDER = {vote: i for i, (vote, _) in enumerate(VOTE_CHOICES)}

    vote = models.CharField(
        max_length=2,
        blank=False,
        choices=VOTE_CHOICES,
        verbose_name=_("vote"),
        help_text=_(
            "Your vote to accept or reject this talk. "
            "More information about the scoring and acceptance criteria "
            "can be found at the GitBook "
            "<a href=\"https://pycontw.github.io/reviewer-guidebook\" "
            "target=\"_blank\">Review Guideline</a>."
        ),
    )

    comment = models.TextField(
        verbose_name=_('comment'),
        help_text=_(
            "Comments to this proposal. This may be available for other "
            "reviewers in later review stages, and you can choose whether "
            "or not to disclose it to the proposal's submitter."
        ),
    )

    DISCLOSE_CHOICES = (
        (True, _('Yes')),
        (False, _('No')),
    )
    discloses_comment = models.BooleanField(
        default=True,
        choices=DISCLOSE_CHOICES,
        verbose_name=_('discloses comment to proposal submitter'),
        help_text=_(
            "Whether the proposal submitter can read you comments. We will "
            "include your comments in the proposal acceptance/rejection "
            "notice sent to the submitter if you allow us to."
        )
    )

    APPROPRIATENESS_CHOICES = (
        (True, _('Yes')),
        (False, _('No')),
    )
    appropriateness = models.BooleanField(
        default=False,
        choices=APPROPRIATENESS_CHOICES,
        verbose_name=_('is appropriate'),
        help_text=_(
            "Administrators can use this field to hide a review from "
            "submitters, even if the reviewer enables disclosure. The review "
            "may be shown to the submitter only if this is set to True."
        ),
    )

    note = models.TextField(
        blank=True,
        verbose_name=_('note'),
        help_text=_(
            "Personal notes about this proposal. You can use this field to "
            "record anything you like during the review process. We promise "
            "to never disclose them to anyone."
        ),
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated'),
        db_index=True,
    )

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        unique_together = ['reviewer', 'stage', 'proposal']
        ordering = ['-updated']

    def __str__(self):
        return ugettext('Review {proposal} by {reviewer}: {vote}').format(
            reviewer=self.reviewer,
            proposal=self.proposal,
            vote=self.get_vote_display(),
        )

    def save(self, *args, **kwargs):
        if self.stage is None:
            self.stage = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.reviews.stage', 0)
        return super().save(*args, **kwargs)

    def is_comment_visible_to_submitter(self):
        return self.discloses_comment and self.appropriateness

    def is_outdated(self):
        return self.updated < self.proposal.last_updated_at


class TalkProposalSnapshot(models.Model):
    """Snapshot for a talk proposal during a review stage.
    """
    proposal = BigForeignKey(
        to=TalkProposal,
        verbose_name=_('proposal'),
        on_delete=models.CASCADE,
    )

    stage = models.IntegerField(
        verbose_name=_('stage'),
    )

    dumped_json = models.TextField(
        verbose_name=_('dumped JSON'),
    )

    dumped_at = models.DateTimeField(
        verbose_name=_('dumped at'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('talk proposal snapshot')
        verbose_name_plural = _('talk proposal snapshots')
        unique_together = ['proposal', 'stage']

    def __str__(self):
        return ugettext('Stage {stage} dump for {proposal}').format(
            stage=self.stage,
            proposal=self.proposal,
        )
