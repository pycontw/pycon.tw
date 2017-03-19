from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.html import format_html
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import UpdateView

from core.mixins import FormValidMessageMixin
from proposals.forms import TalkProposalUpdateForm, TutorialProposalUpdateForm
from proposals.models import TalkProposal, TutorialProposal

from .mixins import ProposalEditMixin, UserProfileRequiredMixin


class TalkProposalMixin:
    model = TalkProposal
    form_class = TalkProposalUpdateForm


class TutorialProposalMixin:
    model = TutorialProposal
    form_class = TutorialProposalUpdateForm


class ProposalUpdateView(
        LoginRequiredMixin, UserProfileRequiredMixin,
        ProposalEditMixin, FormValidMessageMixin, UpdateView):

    success_url = reverse_lazy('user_dashboard')

    examples = {
        "novice": {
            "abstract": (_("Abstract Example"), _(
                "For modern human beings, the data in computers are "
                "essentially an external place for storing our memories. "
                "No matter they're photographs of your daily life, "
                "music, videos, or even some data produced for work, "
                "school, research, they're all being stored in computers. "
                "As the time goes by, the folders in computers fall "
                "into a state of chaos. Or in another scenario, "
                "you're managed to manipulate a series of files, "
                "but ended up with changing them one by one using "
                "File Explorer. Well, is there any better methodology? "
                "This talk is going to introduce how you can "
                "\"programmatically\" manipulate directories and files, "
                "using Python and it's built-in module, pathlib. "
                "We'll look at examples from simple ones to complicated "
                "ones, and eventually combine looping and sorting "
                "techniques in Python, to conquer a complicated file "
                "re-categorize problem."
            )),
            "objective": (_("Objective Example"), _(
                "Targeted at people who's a Python beginner, who "
                "tries to solve some daily life problems with programming. "
                "By the time I started to learn programming, I didn't "
                "know where I can use it. It sounds weird at first, "
                "but since I had only limited ability at the beginning, "
                "things like web development or data analysis were "
                "too hard for me to step into.\n\nBut I found out that, "
                "managing data inside a computer is a very practical "
                "starting point, it's easy to see the result, and it "
                "does allow you to solve some problems that are "
                "rather difficult to do by hand. This kind of "
                "step-by-step learning process should be pretty "
                "helpful for beginners."
            )),
            "description": (_("Description Example"), _(
                "In the final example sharing, we'll try to move a "
                "series of images marked with date and file name, "
                "into \"YEAR/MONTH\" patterned directories that "
                "already have data in it, and also rename each "
                "image according to the chronological order."
            )),
            "outline": (_("Outline Example"), _(
                "1. Common situations in data clean-up  [5 min]\n"
                "2. Introduction to pathlib's design  [10 min]\n"
                "  - Using Path object\n"
                "  - Exploring directory structure: Path.iterdir(), "
                ".glob()\n"
                "  - Using Path for changing paths\n"
                "3. Integrate for-loop and sorting  [5 min]\n"
                "  - sorted(key=) usage\n"
                "  - Integrate enumerated, zip to simultaneously "
                "process multiple related files\n"
                "4. Example sharing  [5 min]\n"
            )),
        },
        "intermediate": {
            "abstract": (_("Abstract Example"), _(
                "Nowadays, photographs always contain the information "
                "about the state where the photo was taken, they're "
                "called EXIF. Sometimes when building a blog about "
                "travel notes or nature photography, you'll have to "
                "put information of some EXIF fields under the "
                "pictures of the article, such as camera model, focal, "
                "aperture, shutter, GPS, etc. Sometimes even show "
                "information as a watermark on the image. In this talk, "
                "we're going to build a workflow on automated EXIF "
                "processing. First introduce the usage of exiftool, "
                "and integrate Pillow to reach the effect of watermark. "
                "Finally, we'll take a blog framework, Pelican, as an "
                "example, to build a Pelican plugin that automatically "
                "processes all the photographs in the article."
            )),
            "objective": (_("Objective Example"), _(
                "Targeted at people who'd like to process a batch of "
                "images, and do external processings using their EXIFs. "
                "And use Pelican blog framework to concretely "
                "demonstrate the integration scenario.\n\nWhile I was "
                "writing blog posts, I found out that manipulations "
                "involving processing images can take a huge amount of "
                "time. Thus hope the audiences will get an idea of how "
                "they can build a automated photograph processing "
                "workflow, and focus more on the article itself. "
                "Hope that the audiences will understand how to "
                "process EXIF and additional processing with Python, "
                "and also the framework of Pelican plugins."
            )),
            "description": (_("Description Example"), _(
                "### Third-party libraries used:\n"
                "  - [exiftool] A Perl tool for analyzing EXIF of images\n"
                "  - [Pillow] A Python tool for image processing, formerly "
                "known as PIL (Python Image Library)\n"
                "  - [Pelican] A static site generator in Python\n\n"
                "[exiftool]: http://www.sno.phy.queensu.ca/~phil/exiftool/\n"
                "[Pillow]: http://python-pillow.github.io/\n"
                "[Pelican]: http://blog.getpelican.com/\n"
            )),
            "outline": (_("Outline Example"), _(
                "1. Intro to EXIF and exiftool [5min]\n"
                "2. Usage of Pillow, use it to add watermark [5min]\n"
                "  - Selection of fonts\n"
                "  - Consistency of layout\n"
                "3. Automation [5min]\n"
                "  - Using stdlib to make a batch processing workflow\n"
                "  - Integrating joblib or multiprocessing to parallelize\n"
                "4. Example (using Pelican) [5min]\n"
                "  - Intro to Pelican's plugin system (integration between "
                "template tags and signals)\n"
                "  - Final resulting work\n"
                "5. Q&A [5min]\n"
            )),
        },
    }

    def get_queryset(self):
        return super().get_queryset().filter(submitter=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"examples": self.examples})
        return context


class TalkProposalUpdateView(TalkProposalMixin, ProposalUpdateView):

    template_name = 'proposals/talk_proposal_update.html'

    def get_form_valid_message(self):
        msg = ugettext('Talk proposal <strong>{title}</strong> updated.')
        return format_html(msg, title=self.object.title)


class TutorialProposalUpdateView(TutorialProposalMixin, ProposalUpdateView):

    template_name = 'proposals/tutorial_proposal_update.html'

    def get_form_valid_message(self):
        msg = ugettext('Tutorial proposal <strong>{title}</strong> updated.')
        return format_html(msg, title=self.object.title)


class ReadonlyProposalUpdateView(
        LoginRequiredMixin, UserProfileRequiredMixin,
        FormValidMessageMixin, UpdateView):

    http_method_names = ['get', 'options']

    def get_queryset(self):
        return super().get_queryset().filter_viewable(self.request.user)

    def get_form(self):
        form = super().get_form()
        for field in form.fields.values():
            field.disabled = True
            field.help_text = ''
        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['readonly'] = True
        return data


class ReadonlyTalkProposalUpdateView(
        TalkProposalMixin, ReadonlyProposalUpdateView):
    template_name = 'proposals/talk_proposal_peek.html'


class ReadonlyTutorialProposalUpdateView(
        TutorialProposalMixin, ReadonlyProposalUpdateView):
    template_name = 'proposals/tutorial_proposal_peek.html'
