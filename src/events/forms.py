from django import forms

from .models import CustomEvent, Schedule

from ccip.models import Venue


class ScheduleCreationForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['html']


class CustomEventForm(forms.ModelForm):

    class Meta:
        model = CustomEvent
        fields = [
            'conference', 'title', 'begin_time', 'end_time', 'location',
            'break_event',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].strip = False

class CommunityTrackForm(forms.Form):
    venue = forms.ModelChoiceField(queryset=Venue.objects.all())
    attendee_token = forms.CharField()
    selected_time = forms.DateTimeField()
