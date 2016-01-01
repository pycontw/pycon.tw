import pytest

from proposals.forms import AdditionalSpeakerCreateForm
from proposals.models import AdditionalSpeaker


@pytest.fixture(params=['talk_proposal', 'tutorial_proposal'])
def proposal(request, talk_proposal, tutorial_proposal):
    return locals()[request.param]


@pytest.fixture
def additional_speaker(another_user, proposal):
    speaker = AdditionalSpeaker.objects.create(
        user=another_user, proposal=proposal,
    )
    return speaker


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
    request.user = user
    form = AdditionalSpeakerCreateForm(
        request=request, proposal=proposal,
        data={'email': another_user.email},
    )
    assert form.is_valid()

    after = form.save()
    assert after == cancelled_additional_speaker
    assert not after.cancelled
