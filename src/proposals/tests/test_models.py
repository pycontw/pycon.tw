from proposals.models import PrimarySpeaker


def test_speaker_compatibility(user, proposal, additional_speaker):
    speaker = PrimarySpeaker(proposal=proposal)
    assert speaker.user == user

    assert speaker.proposal == proposal
    assert additional_speaker.proposal == proposal

    assert not speaker.cancelled
    assert not additional_speaker.cancelled

    assert speaker.get_status_display() == 'Proposal author'
    assert additional_speaker.get_status_display() == 'Pending'


def test_proposal_speakers(user, proposal, additional_speaker):
    assert list(proposal.speakers) == [
        PrimarySpeaker(proposal=proposal), additional_speaker,
    ]
