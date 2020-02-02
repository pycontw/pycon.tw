from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User
from .forms import AdminUserChangeForm, UserCreationForm


@admin.register(User)
class UserAdmin(UserAdmin):

    fieldsets = (
        (
            None,
            {'fields': ('email', 'password')}
        ),
        (
            _('Personal info'),
            {
                'fields': (
                    'speaker_name', 'bio', 'photo',
                    'twitter_id', 'github_id', 'facebook_profile_url',
                ),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'verified', 'is_active', 'is_staff', 'is_superuser',
                    'groups', 'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {'fields': ('last_login', 'date_joined')},
        ),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'email', 'password1', 'password2',
                    'speaker_name', 'bio', 'verified',
                ),
            },
        ),
    )

    form = AdminUserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_staff', 'as_hash')
    list_filter = (
        'verified', 'is_active', 'is_staff', 'is_superuser',
        'groups',
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
