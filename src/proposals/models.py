from django.conf import settings
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation,
)
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext, ugettext_lazy as _

from core.models import (
    ConferenceRelated, DefaultConferenceManager,
    BigForeignKey, EAWTextField, EventInfo,
)


class PrimarySpeaker:
    """A wapper representing the submitter of the proposal as a speaker.

    This class is meant to be compatible with ``AdditionalSpeaker``, and used
    along side with instances of that class.
    """
    def __init__(self, *, proposal=None, user=None):
        if proposal is None and user is None:
            raise ValueError('must specify either proposal or user')
        super().__init__()
        self._proposal = proposal
        self._user = user or proposal.submitter

    def __repr__(self):
        return '<PrimarySpeaker: {name}>'.format(name=self.user.speaker_name)

    def __eq__(self, other):
        return (
            isinstance(other, PrimarySpeaker) and
            self.user == other.user and
            self.proposal == other.proposal
        )

    @property
    def user(self):
        return self._user

    @property
    def proposal(self):
        return self._proposal

    @property
    def cancelled(self):
        return False

    def get_status_display(self):
        return ugettext('Proposal author')


class AdditionalSpeaker(models.Model):

    user = BigForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
    )

    proposal_type = models.ForeignKey(
        to='contenttypes.ContentType',
        verbose_name=_('proposal model type'),
    )
    proposal_id = models.BigIntegerField(
        verbose_name=_('proposal ID'),
    )
    proposal = GenericForeignKey('proposal_type', 'proposal_id')

    SPEAKING_STATUS_PENDING = 'pending'
    SPEAKING_STATUS_ACCEPTED = 'accepted'
    SPEAKING_STATUS_DECLINED = 'declined'
    SPEAKING_STATUS = (
        (SPEAKING_STATUS_PENDING,  _('Pending')),
        (SPEAKING_STATUS_ACCEPTED, _('Accepted')),
        (SPEAKING_STATUS_DECLINED, _('Declined')),
    )
    status = models.CharField(
        max_length=8,
        choices=SPEAKING_STATUS,
        default=SPEAKING_STATUS_PENDING,
    )

    cancelled = models.BooleanField(
        verbose_name=_('cancelled'),
        default=False,
        db_index=True,
    )

    class Meta:
        unique_together = ['user', 'proposal_type', 'proposal_id']
        ordering = ['proposal_type', 'proposal_id', 'pk']
        verbose_name = _('additional speaker')
        verbose_name_plural = _('additional speakers')

    def __str__(self):
        return '{name} ({status})'.format(
            name=self.user.speaker_name,
            status=self.get_status_display(),
        )


class ProposalQuerySet(models.QuerySet):

    def filter_accepted(self):
        return self.filter(accepted=True)

    def filter_viewable(self, user):
        return self.filter(
            Q(submitter=user) |
            Q(additionalspeaker_set__in=user.cospeaking_info_set.all())
        )

    def filter_reviewable(self, user):
        return self.exclude(
            Q(cancelled=True) |
            Q(submitter=user) |
            Q(additionalspeaker_set__in=user.cospeaking_info_set.all())
        )


class AbstractProposal(ConferenceRelated, EventInfo):

    submitter = BigForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_('submitter'),
    )

    objective = EAWTextField(
        verbose_name=_('objective'),
        max_length=1000,
        help_text=_(
            "Who is the intended audience for your talk? (Be specific, "
            "\"Python users\" is not a good answer). "
            "And what will the attendees get out of your talk? When they "
            "leave the room, what will they learn that they didn't know "
            "before? This is NOT made public and for REVIEW ONLY."
        ),
    )

    supplementary = models.TextField(
        verbose_name=_('supplementary'),
        blank=True,
        default='',
        help_text=_(
            "Anything else you'd like the program committee to know when "
            "making their selection: your past speaking experience, community "
            "experience, etc. This is NOT made public and for REVIEW ONLY. "
            "Edit using "
            "<a href='http://daringfireball.net/projects/markdown/basics' "
            "target='_blank'>Markdown</a>."
        ),
    )

    cancelled = models.BooleanField(
        verbose_name=_('cancelled'),
        default=False,
        db_index=True,
    )

    additionalspeaker_set = GenericRelation(
        to=AdditionalSpeaker,
        content_type_field='proposal_type',
        object_id_field='proposal_id',
    )

    objects = DefaultConferenceManager.from_queryset(ProposalQuerySet)()
    all_objects = models.Manager.from_queryset(ProposalQuerySet)()

    class Meta:
        abstract = True

    @property
    def speakers(self):
        yield PrimarySpeaker(proposal=self)
        additionals = self.additionalspeaker_set.filter(cancelled=False)
        for speaker in additionals.select_related('user'):
            yield speaker

    @property
    def speaker_count(self):
        return self.additionalspeaker_set.filter(cancelled=False).count() + 1


class TalkProposal(AbstractProposal):

    DURATION_CHOICES = (
        ('NOPREF', _('No preference')),
        ('PREF25', _('Prefer 25min')),
        ('PREF45', _('Prefer 45min')),
    )
    duration = models.CharField(
        verbose_name=_('duration'),
        max_length=6,
        choices=DURATION_CHOICES,
    )

    outline = models.TextField(
        verbose_name=_('outline'),
        blank=True,
        help_text=_(
            "How the talk will be arranged. It is highly recommended to "
            "attach the estimated time length for each sections in the talk. "
            "Talks in favor of 45min should have a fallback plan about how "
            "to shrink the content into a 25min one. Edit using "
            "<a href='http://daringfireball.net/projects/markdown/basics' "
            "target='_blank'>Markdown</a>."
            "This is NOT made public and for REVIEW ONLY."
        ),
    )

    ACCEPTED_CHOICES = (
        (None,  '----------'),
        (True,  _('Accepted')),
        (False, _('Rejected')),
    )
    accepted = models.NullBooleanField(
        verbose_name=_('accepted'),
        default=None,
        choices=ACCEPTED_CHOICES,
        db_index=True,
    )

    class Meta(AbstractProposal.Meta):
        verbose_name = _('talk proposal')
        verbose_name_plural = _('talk proposals')

    def get_peek_url(self):
        return reverse('talk_proposal_peek', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('talk_proposal_update', kwargs={'pk': self.pk})

    def get_cancel_url(self):
        return reverse('talk_proposal_cancel', kwargs={'pk': self.pk})

    def get_manage_speakers_url(self):
        return reverse('talk_proposal_manage_speakers', kwargs={'pk': self.pk})

    def get_remove_speaker_url(self, speaker):
        return reverse('talk_proposal_remove_speaker', kwargs={
            'pk': self.pk, 'email': speaker.user.email,
        })


class TutorialProposal(AbstractProposal):

    DURATION_CHOICES = (
        ('HALFDAY', _('Half day')),
        ('FULLDAY', _('Full day')),
    )
    duration = models.CharField(
        verbose_name=_('duration'),
        max_length=7,
        choices=DURATION_CHOICES,
    )

    outline = models.TextField(
        verbose_name=_('outline'),
        blank=True,
        help_text=_(
            "How the tutorial will be arranged. You should enumerate over "
            "each section in your talk and attach each section with the "
            "estimated time length. Edit using "
            "<a href='http://daringfireball.net/projects/markdown/basics' "
            "target='_blank'>Markdown</a>."
            "This is NOT made public and for REVIEW ONLY."
        ),
    )

    class Meta(AbstractProposal.Meta):
        verbose_name = _('tutorial proposal')
        verbose_name_plural = _('tutorial proposals')

    def get_peek_url(self):
        return reverse('tutorial_proposal_peek', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('tutorial_proposal_update', kwargs={'pk': self.pk})

    def get_cancel_url(self):
        return reverse('tutorial_proposal_cancel', kwargs={'pk': self.pk})

    def get_manage_speakers_url(self):
        return reverse('tutorial_proposal_manage_speakers', kwargs={
            'pk': self.pk,
        })

    def get_remove_speaker_url(self, speaker):
        return reverse('tutorial_proposal_remove_speaker', kwargs={
            'pk': self.pk, 'email': speaker.user.email,
        })
