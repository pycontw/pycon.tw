from django.utils import timezone

from import_export import fields, resources, widgets

from .models import Time, CustomEvent


class TimeResource(resources.ModelResource):
    class Meta:
        model = Time
        fields = ['value']
        export_order = fields
        import_id_fields = ['value']


class LocalDateTimeWidget(widgets.ForeignKeyWidget):
    def render(self, value, obj=None):
        return timezone.localtime(super().render(value, obj))


class CustomEventResource(resources.ModelResource):
    begin_time = fields.Field(column_name='begin_time', attribute='begin_time', widget=LocalDateTimeWidget(Time, 'value'))
    end_time = fields.Field(column_name='end_time', attribute='end_time', widget=LocalDateTimeWidget(Time, 'value'))

    class Meta:
        model = CustomEvent
        fields = [
            'title', 'break_event', 'location', 'begin_time', 'end_time',
        ]
        export_order = fields
        import_id_fields = ['title', 'begin_time', 'end_time']
