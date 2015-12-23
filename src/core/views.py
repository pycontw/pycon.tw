from django.http import Http404
from django.template.loader import TemplateDoesNotExist, get_template
from django.views.generic import TemplateView


class FlatPageView(TemplateView):

    def get(self, request, *args, **kwargs):
        self.path = kwargs['path']
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        """Look up template from path.

        Template name is built from the path, with leading and trailing
        slashes stripped, "contents/" prepended, and ".html" appended.
        Examples:

        * "/speaking/cfp/"        -> "contents/speaking/cfp.html"
        * "overview/pycontw2016/" -> "contents/overview/pycontw2016.html"

        If a matching template is not found, HTTP 404 will be raised.

        To get a URL to a particular page, use something like
        ``{% url 'page' path='speaking/cfp' %}`` or
        ``reverse('page', kwargs={'path': 'speaking/cfp'})``

        For implementation convinience, template paths with any component
        starting with an underscore will be ignored, and cannot be accessed
        here. This avoids the visitor seeing (accidentally) pages like
        "speaking/base.html".
        """
        template_name = 'contents/' + self.path.strip('/') + '.html'
        if any(c.startswith('_') for c in template_name.split('/')):
            raise Http404
        try:
            get_template(template_name, using=self.template_engine)
        except TemplateDoesNotExist:
            raise Http404
        return [template_name]


flat_page = FlatPageView.as_view()
