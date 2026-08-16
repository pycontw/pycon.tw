from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CustomEvent

CUSTOM_LOCATION = '__custom__'


class CustomEventForm(forms.ModelForm):
    location_mode = forms.ChoiceField(
        label=_('location'),
        required=False,
    )
    custom_location = forms.CharField(
        label=_('custom location'),
        max_length=CustomEvent._meta.get_field('location').max_length,
        required=False,
    )

    class Meta:
        model = CustomEvent
        fields = [
            'conference', 'title', 'begin_time', 'end_time', 'location_mode',
            'custom_location', 'break_event', 'description', 'link_path',
        ]

    class Media:
        js = ('events/admin/custom_event.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        location_choices = list(CustomEvent.LOCATION_CHOICES)
        self.fields['location_mode'].choices = [
            ('', '---------'),
            *location_choices,
            (CUSTOM_LOCATION, _('Custom…')),
        ]
        self.fields['title'].strip = False

        location = self.instance.location
        if location in dict(location_choices):
            self.fields['location_mode'].initial = location
        elif location:
            self.fields['location_mode'].initial = CUSTOM_LOCATION
            self.fields['custom_location'].initial = location

    def clean(self):
        cleaned_data = super().clean()
        location_mode = cleaned_data.get('location_mode')

        if location_mode == CUSTOM_LOCATION:
            location = cleaned_data.get('custom_location')
            if not location:
                self.add_error(
                    'custom_location',
                    _('Enter a custom location.'),
                )
        else:
            location = location_mode

        self.instance.location = location or None
        return cleaned_data
