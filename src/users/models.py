import datetime

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.core import signing
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _

from core.utils import format_html_lazy
from core.models import EAWTextField


class UserQueryset(models.QuerySet):
    """Custom queryset for User.
    """
    def get_valid_speakers(self):
        """Filter only valid speakers from the queryset.

        :seealso: ``User.is_valid_speaker``
        """
        users = self.filter(verified=True, is_active=True)
        users = users.exclude(speaker_name='').exclude(bio='')
        return users


class UserManager(BaseUserManager.from_queryset(UserQueryset)):
    """Custom manager for User.
    """
    def _create_user(self, email, password, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.EmailUser user: user
        :raise ValueError: email is not set
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        last_login = extra_fields.pop('last_login', now)
        date_joined = extra_fields.pop('date_joined', now)
        user = self.model(
            email=email, last_login=last_login, date_joined=date_joined,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: regular user
        """
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: admin user
        """
        return self._create_user(
            email, password, verified=True,
            is_staff=True, is_superuser=True,
            **extra_fields
        )

    def get_with_verification_key(self, verification_key):
        """Get a user from verification key.
        """
        try:
            username = signing.loads(
                verification_key,
                salt=settings.SECRET_KEY,
            )
        except signing.BadSignature:
            raise self.model.DoesNotExist
        return self.get(**{self.model.USERNAME_FIELD: username})


def photo_upload_to(instance, filename):
    return 'avatars/{pk}/{date}-{filename}'.format(
        pk=instance.pk,
        date=str(datetime.date.today()),
        filename=filename,
    )


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255, unique=True, db_index=True,
    )
    speaker_name = models.CharField(
        verbose_name=_('speaker name'),
        max_length=100,
    )
    bio = EAWTextField(
        verbose_name=_('biography'),
        max_length=1000,
        help_text=_(
            "Describe yourself with 500 characters or less. "
            "There will be no formatting."
        ),
    )
    photo = models.ImageField(
        verbose_name=_('photo'),
        blank=True, default='', upload_to=photo_upload_to,
    )
    facebook_profile_url = models.URLField(
        verbose_name=_('Facebook'),
        blank=True,
        help_text=format_html_lazy(_(
            "Link to your Facebook profile page. This will be shown when "
            "we display your public information. If you do not know what your "
            "profile page link is, click on "
            "<a href='https://www.facebook.com/me' "
            "target='_blank' rel='noopener'>this link</a>, and copy-paste the "
            "URL of the page opened. Remember to log in to Facebook first!"
        )),
    )
    twitter_id = models.CharField(
        verbose_name=_('Twitter'),
        blank=True, max_length=100, validators=[
            RegexValidator(r'^[0-9a-zA-Z_]*$', 'Not a valid Twitter handle'),
        ],
        help_text=_(
            "Your Twitter handle, without the \"@\" sign. This will be "
            "shown when we display your public information."
        ),
    )
    github_id = models.CharField(
        verbose_name=_('GitHub'),
        blank=True, max_length=100, validators=[
            RegexValidator(r'^[0-9a-zA-Z_-]*$', 'Not a valid GitHub account'),
        ],
        help_text=_(
            "Your GitHub account, without the \"@\" sign. This will be "
            "shown when we display your public information."
        ),
    )
    verified = models.BooleanField(
        verbose_name=_('verified'),
        default=False,
        help_text=_(
            "Designates whether the user has verified email ownership."
        ),
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_('date joined'),
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.speaker_name

    def get_short_name(self):
        return self.speaker_name

    def is_valid_speaker(self):
        """Whether the user is a valid speaker.

        :seealso: ``UserQuerySet.get_valid_speakers``
        """
        return (
            self.verified and self.is_active and
            self.speaker_name and self.bio
        )

    def is_reviewer(self):
        return self.has_perm('reviews.add_review')

    @property
    def cospeaking_info_set(self):
        return self.additionalspeaker_set.filter(
            cancelled=False,
            conference=settings.CONFERENCE_DEFAULT_SLUG,
        )

    @property
    def twitter_profile_url(self):
        return 'https://twitter.com/{}'.format(self.twitter_id)

    @property
    def github_profile_url(self):
        return 'https://github.com/{}'.format(self.github_id)

    def get_verification_key(self):
        key = signing.dumps(
            obj=getattr(self, self.USERNAME_FIELD),
            salt=settings.SECRET_KEY,
        )
        return key

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def send_verification_email(self, request):
        verification_key = self.get_verification_key()
        verification_url = request.build_absolute_uri(
            reverse('user_verify', kwargs={
                'verification_key': verification_key,
            }),
        )
        context = {
            'user': self,
            'host': request.get_host(),
            'verification_key': verification_key,
            'verification_url': verification_url,
        }
        message = render_to_string(
            'registration/verification_email.txt', context,
        )
        self.email_user(
            subject=ugettext('Verify your email address on {host}').format(
                **context
            ),
            message=message, fail_silently=False,
        )
