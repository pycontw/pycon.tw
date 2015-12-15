from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import ugettext

from .decorators import user_profile_required
from .forms import TalkProposalCreateForm, TalkProposalUpdateForm
from .models import TalkProposal


@login_required
@user_profile_required
def talk_proposal_create(request):
    if request.method == 'POST':
        form = TalkProposalCreateForm(request=request, data=request.POST)
        if form.is_valid():
            proposal = form.save()
            messages.success(request, ugettext('Talk proposal created.'))
            return redirect('talk_proposal_update', pk=proposal.pk)
    else:
        form = TalkProposalCreateForm()
    return render(request, 'proposals/talk_proposal_create.html', {
        'form': form,
    })


@login_required
@user_profile_required
def talk_proposal_update(request, pk):
    try:
        proposal = TalkProposal.objects.get(pk=pk, submitter=request.user)
    except TalkProposal.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = TalkProposalUpdateForm(instance=proposal, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ugettext('Talk proposal updated.'))
            return redirect('user_dashboard')
    else:
        form = TalkProposalUpdateForm(instance=proposal)
    return render(request, 'proposals/talk_proposal_update.html', {
        'form': form,
    })
