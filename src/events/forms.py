from django import forms

from .models import Schedule


class ScheduleCreationForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['html']
