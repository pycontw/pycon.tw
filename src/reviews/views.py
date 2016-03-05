from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .models import TalkProposal
from .models import Review


class TalkProposalListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = TalkProposal
    permission_required = 'reviews.add_review'
    template_name = 'reviews/talkproposal_list.html'


class TalkProposalDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = TalkProposal
    permission_required = 'reviews.add_review'


