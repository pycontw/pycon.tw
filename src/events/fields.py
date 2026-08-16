from django import forms
from django.core import exceptions
from django.db import models
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

CUSTOM_LOCATION = '__custom__'


class EventLocationWidget(forms.MultiWidget):

    def __init__(self, choices, max_length, attrs=None):
        widgets = [
            forms.Select(
                choices=choices,
                attrs={'class': 'event-location-mode'},
            ),
            forms.TextInput(attrs={
                'class': 'vTextField event-location-custom',
                'maxlength': max_length,
                'placeholder': _('custom location'),
            }),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        location_choices = dict(self.widgets[0].choices)
        if value in location_choices:
            return [value, '']
        if value:
            return [CUSTOM_LOCATION, value]
        return ['', '']

    class Media:
        css = {'all': ('events/admin/event_location.css',)}
        js = ('events/admin/event_location.js',)


class EventLocationField(forms.MultiValueField):

    def __init__(self, choices, max_length, **kwargs):
        choices = [
            ('', '---------'),
            *choices,
            (CUSTOM_LOCATION, _('Custom…')),
        ]
        fields = [
            forms.ChoiceField(choices=choices, required=False),
            forms.CharField(max_length=max_length, required=False),
        ]
        kwargs.setdefault('label', _('location'))
        kwargs.setdefault('required', False)
        super().__init__(
            fields=fields,
            require_all_fields=False,
            widget=EventLocationWidget(choices, max_length),
            **kwargs,
        )

    def compress(self, data_list):
        if not data_list:
            return None

        location_mode, custom_location = data_list
        if location_mode == CUSTOM_LOCATION:
            if not custom_location:
                raise exceptions.ValidationError(_('Enter a custom location.'))
            return custom_location
        return location_mode or None


class EventLocationModelField(models.CharField):

    def formfield(self, **kwargs):
        defaults = {
            'choices': self.choices,
            'max_length': self.max_length,
            'label': capfirst(self.verbose_name),
            'required': not self.blank,
            'help_text': self.help_text,
        }
        defaults.update(kwargs)
        return EventLocationField(**defaults)

    def validate(self, value, model_instance):
        if not self.editable:
            return
        if value is None and not self.null:
            raise exceptions.ValidationError(
                self.error_messages['null'],
                code='null',
            )
        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(
                self.error_messages['blank'],
                code='blank',
            )

    def deconstruct(self):
        name, _, args, kwargs = super().deconstruct()
        return name, 'django.db.models.CharField', args, kwargs
