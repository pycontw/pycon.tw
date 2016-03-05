from django.db import models

from users.models import User
from proposals.models import TalkProposal

from .apps import ReviewsConfig


class Review(models.Model):
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-updated']

    def __unicode__(self):
        return u'{0} Review {1}. Score {2}'.format(
            self.user, self.proposal, self.get_score_display()
        )

    REVIEW_CHOICES = (
        (4, '+1'),
        (3, '+0'),
        (2, '-0'),
        (1, '-1'),
        (0, 'Undecided'),
    )

    reviewer = models.ForeignKey(User)
    stage = models.IntegerField(default=1)
    proposal = models.ForeignKey(TalkProposal)
    score = models.IntegerField('Score', default=0, choices=REVIEW_CHOICES)
    comment = models.TextField()
    note = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.stage = ReviewsConfig.stage
        super(Review, self).save(*args, **kwargs)
