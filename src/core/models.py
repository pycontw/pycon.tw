from django.apps import apps
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import format_html_lazy
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

    detailed_description = models.TextField(
        verbose_name=_('detailed description'),
        blank=True,
        help_text=_(
            "Try not be too lengthy to scare away reviewers or potential "
            "audience. A comfortable length is less than 2000 characters "
            "(or about 1200 Chinese characters). Since most reviewers may not "
            "understand the topic as deep as you do, including related links "
            "to the talk topic will help reviewers understand the proposal. "
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
        help_text=format_html_lazy(
            _("Whether you agree to give permission to PyCon Taiwan to "
              "record, edit, and release audio and video of your "
              "presentation. More information can be found at "
              "<a href='{recording_policy_url}' target='_blank'>"
              "Recording Release</a> page."),
            recording_policy_url=reverse_lazy(
                'page', kwargs={'path': 'speaking/recording'},
            )
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

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title
