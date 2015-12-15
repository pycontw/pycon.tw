from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TalkProposal(models.Model):
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
            "domain knowledge please state it here. If yout talk is accepted, "
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

    detailed_description = models.TextField(
        verbose_name=_('detailed description'),
        help_text=_(
            "Description of your talk. Will be made public if your "
            "proposal is accepted. Edit using "
            "<a href='http://daringfireball.net/projects/markdown/basics' "
            "target='_blank'>Markdown</a>."
        ),
    )

    outline = models.TextField(
        verbose_name=_('outline'),
        help_text=_(
            "Tell the reviewers about your talk. Try not be too lengthy, or "
            "you could scare away many reviewers. A comfortable length is "
            "less than 1000 characters (or about 650 Chinese characters). "
            "Including related links will help reviewers understand and more "
            "likely accept the proposal. Note that most reviewers may not "
            "understand the topic as deeply as you do. Edit using "
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
            "experience, etc. This is not made public. Edit using "
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

    class Meta:
        verbose_name = _('talk proposal')
        verbose_name_plural = _('talk proposals')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
