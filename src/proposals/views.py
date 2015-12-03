from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import ugettext

from .decorators import user_profile_required
from .forms import ProposalCreateForm, ProposalUpdateForm
from .models import Proposal


@login_required
@user_profile_required
def proposal_create(request):
    if request.method == 'POST':
        form = ProposalCreateForm(request=request, data=request.POST)
        if form.is_valid():
            proposal = form.save()
            messages.success(request, ugettext('Proposal created.'))
            return redirect('proposal_update', pk=proposal.pk)
    else:
        form = ProposalCreateForm()
    return render(request, 'proposals/proposal_create.html', {'form': form})


@login_required
@user_profile_required
def proposal_update(request, pk):
    try:
        proposal = Proposal.objects.get(pk=pk, submitter=request.user)
    except Proposal.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = ProposalUpdateForm(instance=proposal, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ugettext('Proposal updated.'))
            return redirect('user_dashboard')
    else:
        form = ProposalUpdateForm(instance=proposal)
    return render(request, 'proposals/proposal_update.html', {'form': form})
