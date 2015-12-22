from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractProposal(models.Model):

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
        verbose_name=_('python level'),
        max_length=12,
        choices=PYTHON_LVL_CHOICES,
        help_text=_(
            "The choice of talk level matters during the review process. "
            "More definition of talk level can be found at the <a "
            "href=\"/speaking/talk/\" target=\"_blank\">How to Propose a "
            "talk</a> page. Note that a proposal won't be more likely to be "
            "accepted because of being \"Novice\" level. We may contact you "
            "to change the talk level when we find the content is too-hard "
            "or too-easy for the target audience."
        ),
    )

    objective = models.TextField(
        verbose_name=_('objective'),
        max_length=500,
        help_text=_(
            "What will the attendees get out of your talk? When they leave "
            "the room, what will they learn that they didn't know before?"
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
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title


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
            "to shrink the content into a 25min one."
        ),
    )

    class Meta(AbstractProposal.Meta):
        verbose_name = _('talk proposal')
        verbose_name_plural = _('talk proposals')


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
            "estimated time length."
        ),
    )

    class Meta(AbstractProposal.Meta):
        verbose_name = _('tutorial proposal')
        verbose_name_plural = _('tutorial proposals')
