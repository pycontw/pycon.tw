from datetime import timedelta
import re

import pytest
import pytz
from django.utils.timezone import now
from django.core import mail
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import override_settings

from proposals.models import TalkProposal

taiwan_tz = pytz.timezone('Asia/Taipei')


# Define fixtures

@pytest.fixture()
def today_valid_hour():
    """The valid hour that has been presented today"""
    return taiwan_tz.normalize(now()).hour


def make_proposal_created_earlier(proposal, days=1):
    dt_dayago = now() - timedelta(days=days)
    proposal.created_at = dt_dayago
    proposal.save()


@pytest.fixture()
def dayago_talk_proposal(user):
    proposal = TalkProposal.objects.create(
        id=77,
        submitter=user,
        title='How to build a time machine in 1 day',
        category='SCI'
    )
    make_proposal_created_earlier(proposal)
    return proposal


@pytest.fixture()
def another_user_dayago_talk_proposal(another_user):
    proposal = TalkProposal.objects.create(
        id=9527,
        submitter=another_user,
        title='Transition from Ruby to Python',
        category='CORE',
    )
    make_proposal_created_earlier(proposal)
    return proposal


@pytest.fixture()
def weekago_talk_proposal(user):
    proposal = TalkProposal.objects.create(
        id=56,
        submitter=user,
        title='Long long time ago when Python was still 2.x',
    )
    make_proposal_created_earlier(proposal, days=7)
    return proposal


def test_weekago_talk_created_datetime(weekago_talk_proposal):
    proposal_lifetime = now() - weekago_talk_proposal.created_at
    print('The proposal has been created for %d days' % proposal_lifetime.days)
    assert proposal_lifetime >= timedelta(weeks=1)


def test_recent_proposal_default_command(
    dayago_talk_proposal, weekago_talk_proposal,
    another_user_dayago_talk_proposal,
    today_valid_hour, capsys,
):
    call_command('recent_proposals', hour=today_valid_hour)
    out, err = capsys.readouterr()
    print(out)

    # Test only two talk proposals are retrieved
    assert re.search(r"Got total 2 new proposals", out, re.MULTILINE)
    # Test the title of these two proposals are in the output
    for proposal in [dayago_talk_proposal, another_user_dayago_talk_proposal]:
        assert re.search(proposal.title, out, re.MULTILINE)

    # Test the title of outdated proposals are not in the output
    assert not re.search(weekago_talk_proposal.title, out, re.MULTILINE)


def test_cancelled_proposal_not_shown_in_recent_proposals(
    cancelled_talk_proposal,
    another_user_dayago_talk_proposal,
    weekago_talk_proposal,
    today_valid_hour, capsys,
):
    call_command('recent_proposals', days=6, hour=today_valid_hour)
    out, err = capsys.readouterr()

    # Test only one talk proposal is retrieved
    assert re.search(r"^Got total 1 new proposals", out, re.MULTILINE)
    assert re.search(
        another_user_dayago_talk_proposal.title, out, re.MULTILINE,
    )
    for proposal in [cancelled_talk_proposal, weekago_talk_proposal]:
        assert not re.search(
            proposal.title, out, re.MULTILINE
        )


def test_recent_tutorial_proposals_only(
    tutorial_proposal,
    today_valid_hour, capsys
):
    make_proposal_created_earlier(tutorial_proposal)
    call_command('recent_proposals', hour=today_valid_hour)
    out, err = capsys.readouterr()
    print(out)

    assert 'Talks:\n' not in out
    assert 'Tutorials:\n' in out
    assert re.search(r"^Got total 1 new proposals", out, re.MULTILINE)


# Testing mailing ability

@pytest.mark.parametrize('receivers', [
    ['receiver@pycon.tw'],
    ['receiver@pycon.tw', 'another.receiver@pycon.tw']
])
@override_settings(     # Make sure we don't really send an email.
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='dev@pycon.tw',
)
def test_command_send_mail(
    dayago_talk_proposal,
    today_valid_hour,
    receivers,
):
    call_command(
        'recent_proposals',
        hour=today_valid_hour,
        mailto=receivers,
    )
    assert len(mail.outbox) == 1

    email = mail.outbox[0]
    assert email.from_email == 'dev@pycon.tw'
    assert email.to == receivers
    assert email.subject.startswith(
        '[PyConTW2016][Program] Proposal submission summary'
    )




# Testing edge cases

@pytest.mark.django_db
@pytest.mark.parametrize('days', [-1, 0])
def test_nonpositive_recent_days(days, today_valid_hour):
    with pytest.raises(CommandError) as e:
        call_command('recent_proposals', days=days, hour=today_valid_hour)
    assert 'not a positive number' in str(e.value)


@pytest.mark.django_db
def test_no_recent_proposal(today_valid_hour, capsys):
    call_command('recent_proposals', hour=today_valid_hour)
    out, err = capsys.readouterr()
    print(err)
    assert re.search('^No proposals are recently submitted', out, re.MULTILINE)


def test_justly_created_proposal(talk_proposal, today_valid_hour, capsys):
    call_command('recent_proposals', hour=today_valid_hour)
    out, err = capsys.readouterr()
    assert re.search('^No proposals are recently submitted', out, re.MULTILINE)


@pytest.mark.parametrize('hour', [-1, 25])
def test_invalid_hour(hour):
    with pytest.raises(CommandError) as e:
        call_command('recent_proposals', hour=hour)
    assert 'Given hour %d is invalid' % hour in str(e.value)


@pytest.mark.django_db
def test_default_hour_option(capsys):
    now_dt = taiwan_tz.normalize(now())
    call_command('recent_proposals')
    out, err = capsys.readouterr()
    assert re.search(
        r'to {:%Y-%m-%d %H}:00$'.format(now_dt),
        out, re.MULTILINE
    )


def test_yet_present_hour():
    now_dt = taiwan_tz.normalize(now())
    if now_dt.hour == 23:
        # FIXME: cannot test this between 23:00 - 23:59
        return
    with pytest.raises(CommandError) as e:
        call_command('recent_proposals', hour=now_dt.hour + 1)
    assert 'yet present' in str(e.value)


def test_output_table_trimming(
    another_user_dayago_talk_proposal,
    today_valid_hour, capsys
):
    call_command('recent_proposals', hour=today_valid_hour)
    out, err = capsys.readouterr()
    assert re.search(r'^Python Core \(...\s+', out, re.MULTILINE)
