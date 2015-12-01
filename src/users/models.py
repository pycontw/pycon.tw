from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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
        is_active = extra_fields.pop("is_active", True)
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
    photo = models.FileField(
        verbose_name=_('photo'),
        blank=True, default='', upload_to='documents/%Y/%m/%d',
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

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
