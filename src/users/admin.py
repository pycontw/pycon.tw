from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User


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
                    'twitter_id', 'github_id', 'facebook_id',
                ),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser',
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
                    'speaker_name', 'bio', 'photo',
                    'twitter_id', 'github_id', 'facebook_id',
                ),
            },
        ),
    )

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
