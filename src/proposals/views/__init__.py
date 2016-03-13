from .cancel import TalkProposalCancelView, TutorialProposalCancelView  # noqa
from .create import TalkProposalCreateView, TutorialProposalCreateView  # noqa
from .update import (   # noqa
    TalkProposalUpdateView, TutorialProposalUpdateView,
    ReadonlyTalkProposalUpdateView, ReadonlyTutorialProposalUpdateView,
)

from .speakers import (     # noqa
    AdditionalSpeakerRemoveView, AdditionalSpeakerSetStatusView,
    TalkProposalManageSpeakersView, TutorialProposalManageSpeakersView,
)
