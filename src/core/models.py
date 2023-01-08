import binascii
import os

from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import EAWMaxLengthValidator


class BigForeignKey(models.ForeignKey):
    def db_type(self, connection):
        """ Adds support for foreign keys to big integers as primary keys.

        Django's AutoField is actually an IntegerField (SQL integer field),
        but in some cases we are using bigint on PostgreSQL without Django
        knowing it. So we continue to trick Django here, swapping its field
        type detection, and just tells it to use bigint.

        :seealso: Migrations in the ``postgres`` app.
        """
        presumed_type = super().db_type(connection)
        if apps.is_installed('postgres') and presumed_type == 'integer':
            return 'bigint'
        return presumed_type


class EAWTextField(models.TextField):
    """Derived TextField that checks for its content's EAW lengh.

    This adds an extra validator that counts EAW wide characters as two
    instead of one.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.max_length is not None:
            self.validators.append(EAWMaxLengthValidator(self.max_length))


class DefaultConferenceManagerMixin:
    """Mixin for querysets that provides conference filtering by default.
    """
    conference_attr = 'conference'

    def get_queryset(self):
        """Filter to include only instances for the current conference.

        Note that we use the slug setting directly to minimize SQL overhead.
        """
        qs = super().get_queryset()
        qs = qs.filter(**{
            self.conference_attr: settings.CONFERENCE_DEFAULT_SLUG,
        })
        return qs


class DefaultConferenceManager(DefaultConferenceManagerMixin, models.Manager):
    """A concrete manager using ``DefaultConferenceManagerMixin``.
    """


class ConferenceRelated(models.Model):
    """Mixin providing conference field.
    """
    conference = models.SlugField(
        default=settings.CONFERENCE_DEFAULT_SLUG,
        choices=settings.CONFERENCE_CHOICES,
        verbose_name=_('conference'),
    )

    objects = DefaultConferenceManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True


class EventInfo(models.Model):

    title = models.CharField(
        verbose_name=_('title'),
        max_length=140,
    )

    CATEGORY_CHOICES = (
        ('APPL', _('Application')),
        ('PRAC', _('Best Practices & Patterns')),
        ('COM', _('Community')),
        ('DB', _('Databases')),
        ('DATA', _('Data Analysis')),
        ('EDU', _('Education')),
        ('EMBED', _('Embedded Systems')),
        ('FIN', _('FinTech')),
        ('IOT', _('Internet of Things')),
        ('GAME', _('Gaming')),
        ('GRAPH', _('Graphics')),
        ('ML', _('Machine Learning')),
        ('NLP', _('Natural Language Processing')),
        ('CORE', _('Python Core (language, stdlib, etc.)')),
        ('TOOL', _('Project Tooling')),
        ('SCI', _('Science')),
        ('SEC', _('Security')),
        ('ADMIN', _('Systems Administration')),
        ('TEST', _('Testing')),
        ('WEB', _('Web Frameworks')),
        ('OTHER', _('Other')),
    )
    category = models.CharField(
        verbose_name=_('category'),
        max_length=5,
        choices=CATEGORY_CHOICES,
    )

    LANGUAGE_CHOICES = (
        ('ENEN', _('English talk')),
        ('ZHEN', _('Chinese talk w. English slides')),
    )
    language = models.CharField(
        verbose_name=_('language'),
        max_length=5,
        choices=LANGUAGE_CHOICES,
    )

    talk_language = models.CharField(
        verbose_name=_('Talk language'),
        max_length=32,
    )

    abstract = EAWTextField(
        verbose_name=_('abstract'),
        max_length=1000,
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
    )

    detailed_description = models.TextField(
        verbose_name=_('detailed description'),
        blank=True,
    )

    RECORDING_POLICY_CHOICES = (
        (True, _('Yes')),
        (False, _('No'))
    )
    recording_policy = models.BooleanField(
        verbose_name=_('recording policy'),
        default=True,
        choices=RECORDING_POLICY_CHOICES,
    )

    LIVE_STREAM_POLICY_CHOICES = (
        (True, _('Yes')),
        (False, _('No'))
    )
    live_stream_policy = models.BooleanField(
        verbose_name=_('live stream policy'),
        default=True,
        choices=LIVE_STREAM_POLICY_CHOICES,
    )

    REFERRING_POLICY_CHOICES = (
        (True, _('Yes')),
        (False, _('No'))
    )
    referring_policy = models.BooleanField(
        verbose_name=_('referring policy'),
        default=False,
        choices=REFERRING_POLICY_CHOICES,
    )

    slide_link = models.URLField(
        verbose_name=_('slide link'),
        blank=True,
        default='',
    )

    slido_embed_link = models.URLField(
        verbose_name=_('slido embed link'),
        blank=True,
        default='',
    )

    hackmd_embed_link = models.URLField(
        verbose_name=_('HackMD embed link'),
        blank=True,
        default='',
    )

    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
        db_index=True,
    )

    last_updated_at = models.DateTimeField(
        verbose_name=_('last updated at'),
        auto_now=True,
    )

    PERFER_TIME_CHOICES = (
        ('DAY_ONE_MORNING', _('Day 1, September 2nd, 2023 Morning')),
        ('DAY_ONE_AFTERNOON', _('Day 1, September 2nd, 2023 Afternoon')),
        ('DAY_TWO_MORNING', _('Day 2, September 3rd, 2023 Morning')),
        ('DAY_TWO_AFTERNOON', _('Day 2, September 3rd, 2023 Afternoon')),
    )
    prefer_time = models.CharField(
        verbose_name=_('prefer event time'),
        max_length=32,
        choices=PERFER_TIME_CHOICES,
    )

    LIVING_IN_TAIWAN_CHOICES = (
        (True, _('Yes')),
        (False, _('No'))
    )
    living_in_taiwan = models.BooleanField(
        verbose_name=_('living in Taiwan'),
        default=False,
        choices=REFERRING_POLICY_CHOICES,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_language_tag(self):
        return {
            'ENEN': 'E',
            'ZHEN': 'ZE',
            'ZHZH': 'Z',
        }[self.language]

    def get_python_level_tag(self):
        return {
            'NOVICE': '–',
            'INTERMEDIATE': '=',
            'EXPERIENCED': '≡',
        }[self.python_level]


class Token(models.Model):
    """
    Customize Token for API Authentication.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = BigForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='auth_token',
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
