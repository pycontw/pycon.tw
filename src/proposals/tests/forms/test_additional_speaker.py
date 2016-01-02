import pytest

from proposals.forms import (
    AdditionalSpeakerCancelForm, AdditionalSpeakerCreateForm,
    AdditionalSpeakerSetStatusForm,
)
from proposals.models import AdditionalSpeaker


@pytest.fixture
def cancelled_additional_speaker(additional_speaker):
    additional_speaker.cancelled = True
    additional_speaker.save()
    return additional_speaker


def test_additional_speaker_create_form(additional_speaker):
    with pytest.raises(ValueError) as ctx:
        AdditionalSpeakerCreateForm(instance=additional_speaker)
    assert str(ctx.value) == (
        'Additional speaker creation form cannot be used with an instance.'
    )


def test_additional_speaker_create_form_instance():
    form = AdditionalSpeakerCreateForm()
    assert list(form.fields) == ['email']


def test_additional_speaker_create_form_no_request(user):
    form = AdditionalSpeakerCreateForm(data={'email': user.email})
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Additional speaker creation requires a request object.',
        ],
        'email': [
            'Additional speaker creation requires a proposal instance.',
        ],
    }


def test_additional_speaker_create_form_invalid_submitter(
        request, invalid_user, proposal, another_user):
    request.user = invalid_user
    form = AdditionalSpeakerCreateForm(
        request=request, proposal=proposal,
        data={'email': another_user.email},
    )
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Only authenticated user with complete speaker profile may '
            'create an additional speaker.',
        ],
    }


def test_additional_speaker_create_form_proposal_not_owned(
        request, user, proposal, another_user):
    request.user = another_user
    form = AdditionalSpeakerCreateForm(
        request=request, proposal=proposal,
        data={'email': another_user.email},
    )
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'User can only add additional speakers to owned proposals.',
        ],
    }


def test_additional_speaker_create_form_invalid_additional_speaker(
        request, user, proposal, another_bare_user):
    request.user = user
    form = AdditionalSpeakerCreateForm(
        request=request, proposal=proposal,
        data={'email': another_bare_user.email},
    )
    assert not form.is_valid()
    assert form.errors == {
        'email': ['No valid speaker found with your selection.'],
    }


def test_additional_speaker_create_form_submitter_as_additional_speaker(
        request, user, proposal):
    request.user = user
    form = AdditionalSpeakerCreateForm(
        request=request, proposal=proposal,
        data={'email': user.email},
    )
    assert not form.is_valid()
    assert form.errors == {
        'email': ['This user is already a speaker for the proposal.'],
    }


def test_additional_speaker_create_form_valid(
        request, user, proposal, another_user):
    request.user = user
    form = AdditionalSpeakerCreateForm(
        request=request, proposal=proposal,
        data={'email': another_user.email},
    )
    assert form.is_valid()

    speaker = form.save()
    assert not speaker.cancelled


def test_additional_speaker_create_form_duplicate_user(
        request, user, proposal, another_user, additional_speaker):
    request.user = user
    form = AdditionalSpeakerCreateForm(
        request=request, proposal=proposal,
        data={'email': another_user.email},
    )
    assert not form.is_valid()
    assert form.errors == {
        'email': ['This user is already a speaker for the proposal.'],
    }


def test_additional_speaker_create_form_cancelled_user(
        request, user, proposal, another_user, cancelled_additional_speaker):
    """If a matching additional speaker already exists, the creation form
    should reuse the same additional speaker instance instead of creating
    a new one.

    The "cancelled" flag of the existing epeaker should be set to False.
    """
    request.user = user
    form = AdditionalSpeakerCreateForm(
        request=request, proposal=proposal,
        data={'email': another_user.email},
    )
    assert form.is_valid()

    after = form.save()
    assert after.pk == cancelled_additional_speaker.pk
    assert not after.cancelled


@pytest.mark.parametrize('form_class', [
    AdditionalSpeakerCancelForm, AdditionalSpeakerSetStatusForm,
])
def test_additional_speaker_update_form_no_instance(form_class):
    with pytest.raises(ValueError) as ctx:
        form_class()
    assert str(ctx.value) == (
        'Additional speaker update form must be initialized with an instance.'
    )


def test_additional_speaker_cancel_form(additional_speaker):
    form = AdditionalSpeakerCancelForm(instance=additional_speaker)
    assert list(form.fields) == ['cancelled']


def test_additional_speaker_cancel_form_save(additional_speaker):
    assert not additional_speaker.cancelled
    form = AdditionalSpeakerCancelForm(
        data={'cancelled': 'true'}, instance=additional_speaker,
    )
    form.save()
    assert AdditionalSpeaker.objects.get(pk=additional_speaker.pk).cancelled
