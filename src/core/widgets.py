from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.html import format_html

from .utils import split_css_class


class CharacterCountedTextarea(forms.Textarea):

    class Media:
        js = ['js/vendors/eastasianwidth.js', 'js/tools/character-counter.js']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_classes = split_css_class(self.attrs.get('class', ''))
        css_classes.add('character-counted')
        self.attrs['class'] = ' '.join(css_classes)


class SimpleMDEWidget(forms.Textarea):

    class Media:
        css = {
            'all': [
                'css/vendors/simplemde.min.css',
                'css/simplemde-setup.css',
            ],
        }
        js = ['js/vendors/simplemde.min.js', 'js/tools/simplemde-setup.js']

    def render(self, name, value, attrs=None, renderer=None):
        attrs = self.build_attrs(attrs, {'name': name})
        if attrs.get('disabled', False):
            return format_html(
                '<div class="editor-readonly">'
                '<div class="editor-preview editor-preview-active">'
                '{content}</div></div>',
                content=value,
            )
        else:
            attrs['data-simplemde'] = True
            return format_html(
                '<textarea{attrs}>\r\n{content}</textarea>',
                attrs=flatatt(attrs), content=force_str(value),
            )
