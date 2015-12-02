from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _


class Proposal(models.Model):
    """Represent a submitted talk proposal.
    """

    submitter = models.ForeignKey(
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
        ('EMBED', _('Embedd Systems')),
        ('GAME',  _('Gaming')),
        ('OTHER', _('Other')),
        ('CORE',  _('Python Core & Internals (language, stdlib, etc.)')),
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

    LANGUAGE_CHOICES = (
        ('ENG', _('English')),
        ('CHI', _('Chinese')),
    )
    language = models.CharField(
        verbose_name=_('language'),
        max_length=3,
        choices=LANGUAGE_CHOICES,
    )

    target_audience = models.CharField(
        verbose_name=_('target audience'),
        max_length=140,
        help_text=_(
            "Who is the intended audience for your talk? (Be specific, "
            "\"Python users\" is not a good answer)"
        ),
    )

    abstract = models.TextField(
        verbose_name=_('abstract'),
        max_length=400,
        help_text=_(
            "The overview of what the talk is about. If the talk assume some "
            "domain knowledge please state it here."
        ),
    )

    PYTHON_LVL_CHOICES = (
        ('NOVICE', _('Novice')),
        ('INTERMEDIATE', _('Intermediate')),
        ('EXPERIENCED', _('Experienced')),
    )
    python_level = models.CharField(
        verbose_name=_('python level'),
        max_length=12,
        choices=PYTHON_LVL_CHOICES,
        help_text=_(
            "The choice of talk level matters during the review process. "
            "More definition of talk level can be found at the Talk Level "
            "Definition in [How to Propose a talk] page. Note that a proposal "
            "who't be more likely to accepted because of being \"Novice\" "
            "level. We may contact you to change the talk level when we find "
            "the contend is too-hard or too-easy for the target audience."
        ),
    )

    objectives = models.TextField(
        verbose_name=_('objectives'),
        help_text=_(
            "What will attendees get out of your talk? When they leave the "
            "room, what will they know that they didn't know before?"
        ),
    )

    detailed_description = models.TextField(
        verbose_name=_('detailed description'),
        help_text=_(
            "Try not be too lengthy which will scare away many reviewers. "
            "A comfortable length is less than 1000 chars (about 650 Chinese "
            "chars). Including related links to the talk topic will help "
            "reviewers understand and more likely accept the proposal. Note "
            "that most reviewers may not understand the topic as deep as you "
            "do."
        ),
    )

    outline = models.TextField(
        verbose_name=_('outline'),
        blank=True,
        default='',
        help_text=_(
            "How the talk will be arranged. It is highly recommended to "
            "attach the estimated time length for each sections in the talk. "
            "Talks in favor of 45min should have a fallback plan about how to "
            "shrink the content into a 25min one."
        ),
    )

    supplementary = models.TextField(
        verbose_name=_('supplementary'),
        blank=True,
        default='',
        help_text=_(
            "Anything else you'd like the program committee to know when "
            "making their selection: your past speaking experience, open "
            "source community experience, etc."
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
            "Description: If you agree to give permission to PyCon Taiwan to "
            "record, edit, and release audio and video of your presentation, "
            "please check this box. See [Recoding Release] for details."
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
        verbose_name = _('proposal')
        verbose_name_plural = _('proposals')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
