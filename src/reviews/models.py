from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import BigForeignKey
from proposals.models import TalkProposal

from .apps import ReviewsConfig


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

    SCORE_CHOICES = (
        (2, _('+1 (strong accept)')),
        (1, _('+0 (weakly accept)')),
        (0, '----------'),
        (-1, _('-0 (weakly reject)')),
        (-2, _('-1 (strong reject)')),
    )
    score = models.SmallIntegerField(
        default=0,
        choices=SCORE_CHOICES,
        verbose_name=_('score'),
        help_text=_(
            "Your score to accept or reject this talk. "
            "More information about the scoring and acceptance criteria "
            "can be found at the google doc "
            "<a href=\"https://goo.gl/EPlUZx\">Review Guideline</a>."
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
        ordering = ['-updated']

    def __str__(self):
        return _('Review {proposal} by {reviewer}: {score}').format(
            reviewer=self.reviewer,
            proposal=self.proposal,
            score=self.get_score_display(),
        )

    def save(self, *args, **kwargs):
        if self.stage is None:
            self.stage = ReviewsConfig.stage
        return super().save(*args, **kwargs)
