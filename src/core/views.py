import functools
import pytz

from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.utils import timezone
from django.views.defaults import page_not_found, server_error
from django.views.generic import TemplateView

from .data import EXTRA_DATA
from .utils import (
    TemplateExistanceStatusResponse,
    collect_language_codes,
)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deadline = datetime(2016, 6, 3, 8, 20)
        now = timezone.now()
        countdown = pytz.timezone('Asia/Taipei').localize(deadline) - now
        context['countdown'] = {
            'type': _('days'),
            'value': countdown.days
        }
        if countdown.days == 0:
            context['countdown']['type'] = _('hours')
            context['countdown']['value'] = countdown.seconds // 3600
        return context


class FlatPageView(TemplateView):

    response_class = TemplateExistanceStatusResponse

    def get(self, request, *args, **kwargs):
        path = self.kwargs['path'].strip('/')
        if not path or any(c.startswith('_') for c in path.split('/')):
            raise Http404
        self.path = path
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(EXTRA_DATA.get(self.path, {}))
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
        template_names = [
            '/'.join(['contents', code, self.path + '.html'])
            for code in collect_language_codes(self.request.LANGUAGE_CODE)
        ]
        return template_names


index = IndexView.as_view()
flat_page = FlatPageView.as_view()


def error_page(request, code):
    """A proxy view displaying error pages.
    """
    try:
        view_func = {
            '404': functools.partial(page_not_found, exception=Http404()),
            '500': server_error,
        }[code]
    except KeyError:
        raise Http404
    return view_func(request)
