from django import forms

from core.utils import TimeRange, time_add

from .models import Event, Talk


class CheckTimeSlotOverlapMixin:

    def _make_time_range(self):
        """This will be called by ``clean`` to get a TimeRange instance.

        Subclasses should override this.
        """
        raise NotImplementedError

    def clean(self):
        data = super().clean() or self.cleaned_data
        timerange = self._make_time_range()
        filter_kwargs = {
            'day': data['day'],
            'location': data['location'],
            'timerange': timerange,
            'exclude': self.instance,
        }
        overlapping_talks = Talk.objects.filter_overlapping(**filter_kwargs)
        overlapping_events = Event.objects.filter_overlapping(**filter_kwargs)
        if overlapping_talks.exists() or overlapping_events.exists():
            raise forms.ValidationError(
                'Given time slot conflicts with existing event.'
            )
        return data


class EventForm(CheckTimeSlotOverlapMixin, forms.ModelForm):
    def _make_time_range(self):
        data = self.cleaned_data
        return TimeRange(start=data['start_time'].time, end=data['end_time'])


class TalkForm(CheckTimeSlotOverlapMixin, forms.ModelForm):
    def _make_time_range(self):
        data = self.cleaned_data
        start_time = data['start_time'].time
        end_time = time_add(data['day'], start_time, data['duration'])
        return TimeRange(start=start_time, end=end_time)
