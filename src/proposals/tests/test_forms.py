from proposals.forms import (
    TalkProposalCreateForm, TalkProposalUpdateForm,
    TutorialProposalCreateForm, TutorialProposalUpdateForm,
)


def test_talk_proposal_create_form():
    form = TalkProposalCreateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language',
        'python_level', 'recording_policy',
    ]


def test_tutorial_proposal_create_form():
    form = TutorialProposalCreateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language',
        'python_level', 'recording_policy',
    ]


def test_talk_proposal_update_form():
    form = TalkProposalUpdateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language', 'target_audience',
        'abstract', 'python_level', 'objective', 'detailed_description',
        'outline', 'supplementary', 'recording_policy', 'slide_link',
    ]


def test_tutorial_proposal_update_form():
    form = TutorialProposalUpdateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language', 'target_audience',
        'abstract', 'python_level', 'objective', 'detailed_description',
        'outline', 'supplementary', 'recording_policy', 'slide_link',
    ]
