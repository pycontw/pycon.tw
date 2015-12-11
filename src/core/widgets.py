from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html


class SimpleMDEWidget(forms.Textarea):

    class Media:
        css = {
            'all': [
                'css/vendors/simplemde.min.css',
                'css/simplemde-setup.css',
            ],
        }
        js = ['js/simplemde.js', 'js/simplemde-setup.js']

    def render(self, name, value, attrs=None):
        attrs = self.build_attrs(attrs, name=name)
        attrs['data-simplemde'] = True
        return format_html(
            '<textarea{attrs}>\r\n{content}</textarea>'.format(
                attrs=flatatt(attrs), content=force_text(value),
            )
        )
