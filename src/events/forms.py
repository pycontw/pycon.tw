from django import forms

from .models import CustomEvent


class CustomEventForm(forms.ModelForm):

    class Meta:
        model = CustomEvent
        fields = [
            'conference', 'title', 'begin_time', 'end_time', 'location',
            'break_event', 'description', 'link_path',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].strip = False
