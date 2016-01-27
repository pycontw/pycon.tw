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

    def get(self, request, *args, **kwargs):
        self.path = kwargs['path']
        return super().get(request, *args, **kwargs)

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
        path = self.path.strip('/')
        if any(c.startswith('_') for c in path.split('/')):
            raise Http404
        template_names = [
            '/'.join(['contents', code, path + '.html'])
            for code in collect_language_codes(self.request.LANGUAGE_CODE)
        ]
        return template_names


class StaffPageView(TemplateView):

    template_name = 'contents/_base/staff.html'

    def get_staff_data(self):
        path = finders.find('data/staff.yml')
        with open(path) as f:
            info = yaml.load(f)
        return info

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(self.get_staff_data())
        return data


index = IndexView.as_view()
flat_page = FlatPageView.as_view()
staff = StaffPageView.as_view()
