import datetime

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.core import signing
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _


class EmailUserManager(BaseUserManager):
    """Custom manager for EmailUser."""

    def _create_user(
            self, email, password, is_staff, is_superuser, **extra_fields):
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
        is_active = extra_fields.pop('is_active', False)
        user = self.model(
            email=email, is_staff=is_staff, is_active=is_active,
            is_superuser=is_superuser, last_login=now, date_joined=now,
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
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(
            email, password, is_staff, False, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: admin user
        """
        return self._create_user(
            email, password, True, True, **extra_fields
        )

    def get_with_activation_key(self, activation_key):
        """Get a user from activation key.
        """
        try:
            username = signing.loads(
                activation_key,
                salt=settings.USER_ACTIVATION_KEY_SALT,
                max_age=settings.USER_ACTIVATION_EXPIRE_SECONDS,
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
    bio = models.TextField(
        verbose_name=_('biography'),
        max_length=140,
        help_text=_("About you. There will be no formatting."),
    )
    photo = models.ImageField(
        verbose_name=_('photo'),
        blank=True, default='', upload_to=photo_upload_to,
    )
    facebook_id = models.CharField(
        verbose_name=_('facebook'),
        blank=True, max_length=100,
    )
    twitter_id = models.CharField(
        verbose_name=_('twitter'),
        blank=True, max_length=100,
    )
    github_id = models.CharField(
        verbose_name=_('github'),
        blank=True, max_length=100,
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
        default=False,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_('date joined'),
        default=timezone.now,
    )

    objects = EmailUserManager()

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

    @property
    def profile_filled(self):
        return self.is_active and self.speaker_name and self.bio

    def get_activation_key(self):
        key = signing.dumps(
            obj=getattr(self, self.USERNAME_FIELD),
            salt=settings.USER_ACTIVATION_KEY_SALT,
        )
        return key

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def send_activation_email(self, request):
        activation_key = self.get_activation_key()
        activation_url = request.build_absolute_uri(
            reverse('user_activate', kwargs={
                'activation_key': activation_key,
            }),
        )

        context = {
            'user': self,
            'activation_key': activation_key,
            'activation_url': activation_url,
        }
        text_message = render_to_string(
            'registration/activation_email.txt', context,
        )
        html_message = render_to_string(
            'registration/activation_email.html', context,
        )
        self.email_user(
            subject=ugettext('Complete your registration on tw.pycon.org'),
            message=text_message, html_message=html_message,
            fail_silently=False,
        )
