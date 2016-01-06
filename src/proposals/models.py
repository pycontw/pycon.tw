from django.conf import settings
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation,
)
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext, ugettext_lazy as _

from core.models import BigForeignKey
from core.utils import format_html_lazy


class PrimarySpeaker:
    """A wapper representing the submitter of the proposal as a speaker.

    This class is meant to be compatible with ``AdditionalSpeaker``, and used
    along side with instances of that class.
    """
    def __init__(self, proposal):
        super().__init__()
        self._proposal = proposal
        self._user = proposal.submitter

    def __repr__(self):
        return '<PrimarySpeaker: {name}>'.format(name=self.user.speaker_name)

    def __eq__(self, other):
        return (
            isinstance(other, PrimarySpeaker) and self.user == other.user
            and self.proposal == other.proposal
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
        ordering = ['proposal_type', 'proposal_id', 'user__speaker_name']
        verbose_name = _('additional speaker')
        verbose_name_plural = _('additional speakers')

    def __str__(self):
        return '{name} ({status})'.format(
            name=self.user.speaker_name,
            status=self.get_status_display(),
        )


class ProposalQuerySet(models.QuerySet):
    def filter_viewable(self, user):
        return self.filter(
            Q(submitter=user)
            | Q(additionalspeaker_set__in=user.additionalspeaker_set.all())
        )


class AbstractProposal(models.Model):

    submitter = BigForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_('submitter'),
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=140,
    )

    CATEGORY_CHOICES = (
        ('PRAC',  _('Best Practices & Patterns')),
        ('COM',   _('Community')),
        ('DB',    _('Databases')),
        ('DATA',  _('Data Analysis')),
        ('EDU',   _('Education')),
        ('EMBED', _('Embedded Systems')),
        ('GAME',  _('Gaming')),
        ('GRAPH', _('Graphics')),
        ('OTHER', _('Other')),
        ('CORE',  _('Python Core (language, stdlib, etc.)')),
        ('INTNL', _('Python Internals')),
        ('LIBS',  _('Python Libraries')),
        ('SCI',   _('Science')),
        ('SEC',   _('Security')),
        ('ADMIN', _('Systems Administration')),
        ('TEST',  _('Testing')),
        ('WEB',   _('Web Frameworks')),
    )
    category = models.CharField(
        verbose_name=_('category'),
        max_length=5,
        choices=CATEGORY_CHOICES,
    )

    LANGUAGE_CHOICES = (
        ('ENG', _('English')),
        ('CHI', _('Chinese')),
    )
    language = models.CharField(
        verbose_name=_('language'),
        max_length=3,
        choices=LANGUAGE_CHOICES,
    )

    abstract = models.TextField(
        verbose_name=_('abstract'),
        max_length=500,
        help_text=_(
            "The overview of what the talk is about. If the talk assume some "
            "domain knowledge please state it here. If your talk is accepted, "
            "this will be displayed on both the website and the handbook. "
            "Should be one paragraph."
        ),
    )

    PYTHON_LVL_CHOICES = (
        ('NOVICE', _('Novice')),
        ('INTERMEDIATE', _('Intermediate')),
        ('EXPERIENCED', _('Experienced')),
    )
    python_level = models.CharField(
        verbose_name=_('Python level'),
        max_length=12,
        choices=PYTHON_LVL_CHOICES,
        help_text=format_html_lazy(
            _("The choice of talk level matters during the review process. "
              "More definition of talk level can be found at the <a href=\""
              "{speaking_talk_url}\" target=\"_blank\">How to Propose a "
              "Talk</a> page. Note that a proposal won't be more likely to be "
              "accepted because of being \"Novice\" level. We may contact you "
              "to change the talk level when we find the content is too-hard "
              "or too-easy for the target audience."),
            speaking_talk_url=reverse_lazy(
                'page', kwargs={'path': 'speaking/talk'},
            ),
        ),
    )

    objective = models.TextField(
        verbose_name=_('objective'),
        max_length=500,
        help_text=_(
            "Who is the intended audience for your talk? (Be specific, "
            "\"Python users\" is not a good answer). "
            "And what will the attendees get out of your talk? When they "
            "leave the room, what will they learn that they didn't know "
            "before? This is NOT made public and for REVIEW ONLY."
        ),
    )

    detailed_description = models.TextField(
        verbose_name=_('detailed description'),
        blank=True,
        help_text=_(
            "Try not be too lengthy to scare away reviewers or potential "
            "audience. A comfortable length is less than 1000 characters "
            "(or about 600 Chinese characters). Since most reviewers may not "
            "understand the topic as deep as you do, including related links "
            "to the talk topic will help reviewers understand the proposal. "
            "Edit using "
            "<a href='http://daringfireball.net/projects/markdown/basics' "
            "target='_blank'>Markdown</a>."
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

    RECORDING_POLICY_CHOICES = (
        (True, _('Yes')),
        (False, _('No'))
    )
    recording_policy = models.BooleanField(
        verbose_name=_('recording policy'),
        default=True,
        choices=RECORDING_POLICY_CHOICES,
        help_text=_(
            "Whether you agree to give permission to PyCon Taiwan to "
            "record, edit, and release audio and video of your presentation."
        ),
    )

    slide_link = models.URLField(
        verbose_name=_('slide link'),
        blank=True,
        default='',
        help_text=_(
            "You can add your slide link near or after the conference day. "
            "Not required for review."
        ),
    )

    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
        db_index=True,
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

    objects = ProposalQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def speakers(self):
        yield PrimarySpeaker(self)
        additionals = self.additionalspeaker_set.filter(cancelled=False)
        for speaker in additionals.select_related('user'):
            yield speaker


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
            "to shrink the content into a 25min one. "
            "This is NOT made public and for REVIEW ONLY."
        ),
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
            "estimated time length. "
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
