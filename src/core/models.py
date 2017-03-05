from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

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
        ('PRAC',  _('Best Practices & Patterns')),
        ('COM',   _('Community')),
        ('DB',    _('Databases')),
        ('DATA',  _('Data Analysis')),
        ('EDU',   _('Education')),
        ('EMBED', _('Embedded Systems')),
        ('FIN',   _('FinTech')),
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
        ('ENEN', _('English talk')),
        ('ZHEN', _('Chinese talk w. English slides')),
        ('ZHZH', _('Chinese talk w. Chinese slides')),
        ('TAI',  _('Taiwanese Hokkien')),
    )
    language = models.CharField(
        verbose_name=_('language'),
        max_length=4,
        choices=LANGUAGE_CHOICES,
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

    slide_link = models.URLField(
        verbose_name=_('slide link'),
        blank=True,
        default='',
    )

    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title
