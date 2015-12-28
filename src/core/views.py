from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import RedirectView, TemplateView

from .utils import (
    TemplateExistanceStatusResponse,
    collect_language_codes,
)


class I18nRedirectView(RedirectView):
    def get_redirect_url(self, path):
        return reverse('page', kwargs={'path': path})


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


index = IndexView.as_view()
i18n_redirect = I18nRedirectView.as_view()
flat_page = FlatPageView.as_view()
