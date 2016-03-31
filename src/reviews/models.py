from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from core.models import BigForeignKey
from proposals.models import TalkProposal

from .apps import ReviewsConfig


REVIEW_REQUIRED_PERMISSIONS = ['reviews.add_review']


class ReviewQuerySet(models.QuerySet):

    def filter_current_reviews(self, proposal, user=None):
        qs = self.filter(proposal=proposal, stage__lte=ReviewsConfig.stage)
        if user:
            qs = qs.exclude(reviewer=user)
        return qs

    def filter_reviewable(self, user):
        cospeaking = user.cospeaking_info_set.all()
        qs = self.exclude(
            Q(proposal__cancelled=True) |
            Q(proposal__accepted__isnull=False) |
            Q(proposal__submitter=user) |
            Q(proposal__additionalspeaker_set__in=cospeaking)
        )
        qs = qs.filter(reviewer=user)
        return qs


class Review(models.Model):

    reviewer = BigForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_('reviewer'),
    )

    stage = models.IntegerField(
        verbose_name=_('stage'),
    )

    proposal = models.ForeignKey(
        to=TalkProposal,
        verbose_name=_('proposal'),
    )

    objects = ReviewQuerySet.as_manager()

    class Vote(object):
        PLUS_ONE = "+1"
        PLUS_ZERO = "+0"
        MINUS_ZERO = "-0"
        MINUS_ONE = "-1"

    VOTE_CHOICES = (
        (Vote.PLUS_ONE, _('+1 (strong accept)')),
        (Vote.PLUS_ZERO, _('+0 (weak accept)')),
        (Vote.MINUS_ZERO, _('-0 (weak reject)')),
        (Vote.MINUS_ONE, _('-1 (strong reject)')),
    )

    vote = models.CharField(
        max_length=2,
        blank=False,
        choices=VOTE_CHOICES,
        verbose_name=_("vote"),
        help_text=_(
            "Your vote to accept or reject this talk. "
            "More information about the scoring and acceptance criteria "
            "can be found at the google doc "
            "<a href=\"https://goo.gl/EPlUZx\" "
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
        return _('Review {proposal} by {reviewer}: {vote}').format(
            reviewer=self.reviewer,
            proposal=self.proposal,
            vote=self.get_vote_display(),
        )

    def save(self, *args, **kwargs):
        if self.stage is None:
            self.stage = ReviewsConfig.stage
        return super().save(*args, **kwargs)
