import yaml

from django.contrib.staticfiles import finders
from django.http import Http404
from django.views.generic import TemplateView

from .utils import (
    TemplateExistanceStatusResponse,
    collect_language_codes,
)


class IndexView(TemplateView):
    template_name = 'index.html'


class FlatPageView(TemplateView):

    response_class = TemplateExistanceStatusResponse

    def get_path_components(self, path):
        components = path.strip('/').split('/')
        if not components or any(c.startswith('_') for c in components):
            raise Http404
        return components

    def load_extra_data(self):
        *components, basename = self.path_components
        path = finders.find(
            '/'.join(['data', 'contents'] + components + [basename + '.yml']),
        )
        if path is None:
            return {}
        with open(path) as f:
            return yaml.load(f)

    def get(self, request, *args, **kwargs):
        self.path_components = self.get_path_components(kwargs['path'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(self.load_extra_data())
        return data

    def get_template_names(self):
        """Look up template from path.

        Template name is built from the path, with leading and trailing
        slashes stripped, language code and "contents/" prepended,
        and ".html" appended.

        Examples:

        * "/speaking/cfp/"    -> "contents/<lang>/speaking/cfp.html"
        * "overview/pycontw/" -> "contents/<lang>/overview/pycontw.html"

        If a matching template is not found, HTTP 404 will be raised.

        To get a URL to a particular page, use something like
        ``{% url 'page' path='speaking/cfp' %}`` or
        ``reverse('page', kwargs={'path': 'speaking/cfp'})``

        For implementation convinience, template paths with any component
        starting with an underscore will be ignored, and cannot be accessed
        here. This avoids the visitor seeing (accidentally) pages like
        "speaking/base.html".
        """
        *components, basename = self.path_components
        template_names = [
            '/'.join(['contents', code] + components + [basename + '.html'])
            for code in collect_language_codes(self.request.LANGUAGE_CODE)
        ]
        return template_names


index = IndexView.as_view()
flat_page = FlatPageView.as_view()
