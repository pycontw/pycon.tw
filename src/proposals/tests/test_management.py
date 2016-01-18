from datetime import timedelta
import re

import pytest
from django.utils.timezone import now
from django.core.management import call_command
from django.core.management.base import CommandError

from proposals.models import TalkProposal


@pytest.fixture()
def weekago_talk_proposal(user):
    dt_weekago = now() - timedelta(weeks=1)
    proposal = TalkProposal.objects.create(
        id=56,
        submitter=user,
        title='Long long time ago when Python was still 2.x',
    )
    proposal.created_at = dt_weekago
    proposal.save()
    return proposal


def test_weekago_talk_created_datetime(weekago_talk_proposal):
    proposal_lifetime = now() - weekago_talk_proposal.created_at
    print('The proposal has been created for %d days' % proposal_lifetime.days)
    assert proposal_lifetime >= timedelta(weeks=1)


@pytest.fixture()
def another_user_dayago_talk_proposal(another_user):
    dt_dayago = now() - timedelta(days=1)
    proposal = TalkProposal.objects.create(
        id=9527,
        submitter=another_user,
        title='Transition from Ruby to Python',
        category='CORE',
        created_at=dt_dayago,
    )
    return proposal


def test_recent_proposal_default_command(
    talk_proposal, weekago_talk_proposal,
    another_user_dayago_talk_proposal,
    capsys,
):
    call_command('recent_proposals')
    out, err = capsys.readouterr()
    print(out)

    # Test only two talk proposals are retrieved
    assert re.search(r"Got total 2 new proposals", out, re.MULTILINE)
    # Test the title of these two proposals are in the output
    for proposal in [talk_proposal, another_user_dayago_talk_proposal]:
        assert re.search(proposal.title, out, re.MULTILINE)

    # Test the title of outdated proposals are not in the output
    assert not re.search(weekago_talk_proposal.title, out, re.MULTILINE)


def test_cancelled_proposal_not_shown_in_recent_proposals(
    cancelled_talk_proposal,
    another_user_dayago_talk_proposal,
    weekago_talk_proposal,
    capsys,
):
    call_command('recent_proposals', recent=6)
    out, err = capsys.readouterr()

    # Test only one talk proposal is retrieved
    assert re.search(r"^Got total 1 new proposals", out, re.MULTILINE)
    assert re.search(another_user_dayago_talk_proposal.title, out, re.MULTILINE)
    for proposal in [cancelled_talk_proposal, weekago_talk_proposal]:
        assert not re.search(
            proposal.title, out, re.MULTILINE
        )


def test_recent_tutorial_proposals_only(tutorial_proposal, capsys):
    call_command('recent_proposals')
    out, err = capsys.readouterr()

    assert 'Talks:\n' not in out
    assert 'Tutorials:\n' in out
    assert re.search(r"^Got total 1 new proposals", out, re.MULTILINE)


@pytest.mark.django_db
@pytest.mark.parametrize('recent_days', [-1, 0])
def test_nonpositive_recent_days(recent_days):
    with pytest.raises(CommandError) as e:
        call_command('recent_proposals', recent=recent_days)
    assert 'Provide positive number' in str(e.value)



@pytest.mark.django_db
def test_no_recent_proposal(capsys):
    call_command('recent_proposals')
    out, err = capsys.readouterr()
    print(err)
    assert re.search('^No proposals are recently submitted', err, re.MULTILINE)


def test_output_table_trimming(another_user_dayago_talk_proposal, capsys):
    call_command('recent_proposals')
    out, err = capsys.readouterr()
    assert re.search(r'^Python Core \(...\s+', out, re.MULTILINE)
