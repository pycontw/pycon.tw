import pytest

from django.contrib.auth import get_user_model
from django.template import Context, Template

from proposals.models import AdditionalSpeaker, TalkProposal


def render_template(template_string, context_data=None):
    context_data = context_data or {}
    return Template(template_string).render(Context(context_data))


@pytest.fixture
def talk_proposals(talk_proposal, user, another_user):
    proposal_0 = TalkProposal.objects.create(
        submitter=another_user, title='Concrete construct saturation',
    )

    proposal_1 = talk_proposal
    AdditionalSpeaker.objects.create(user=another_user, proposal=proposal_1)

    user_3 = get_user_model().objects.create_user(
        email='somebody@email.address', password='19',
        speaker_name='Somebody Somewhere',
    )
    proposal_2 = TalkProposal.objects.create(
        submitter=user_3, title='Render-farm smart-meta-rain-ware',
    )
    AdditionalSpeaker.objects.create(user=another_user, proposal=proposal_2)
    AdditionalSpeaker.objects.create(user=user, proposal=proposal_2)
    return [
        proposal_0,     # Proposal without additional speakers.
        proposal_1,     # Proposal with one additional speaker.
        proposal_2,     # Proposal with two additional speakers.
    ]


def test_speaker_names_display(talk_proposals, parser):
    result = render_template(
        '{% load proposals %}'
        '<ul>'
        '{% for proposal in proposals %}'
        '<li>{{ proposal|speaker_names_display }}</li>'
        '{% endfor %}'
        '</ul>', {'proposals': talk_proposals},
    )
    actual = parser.arrange(parser.parse(text=result, create_parent=False))
    expected = parser.arrange("""
        <ul>
          <li>Misaki Mei</li>
          <li>User and Misaki Mei</li>
          <li>Somebody Somewhere, Misaki Mei and User</li>
        </ul>
    """)
    assert actual == expected
