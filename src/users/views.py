from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm


@login_required
def user_dashboard(request):
    logout_next = reverse('index')
    return render(request, 'users/user_dashboard.html', {
        'logout_next': logout_next,
    })


@login_required
def user_profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/user_profile_update.html', {'form': form})
