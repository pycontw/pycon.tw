from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^submit/$',
        views.ProposalCreateChoiceView.as_view(),
        name='proposal_create_choice'),

    url(r'^talk/submit/$',
        views.TalkProposalCreateView.as_view(),
        name='talk_proposal_create'),
    url(r'^talk/(?P<pk>\d+)/peek/$',
        views.ReadonlyTalkProposalUpdateView.as_view(),
        name='talk_proposal_peek'),
    url(r'^talk/(?P<pk>\d+)/edit/$',
        views.TalkProposalUpdateView.as_view(),
        name='talk_proposal_update'),
    url(r'^talk/(?P<pk>\d+)/cancel/$',
        views.TalkProposalCancelView.as_view(),
        name='talk_proposal_cancel'),
    url(r'^talk/(?P<pk>\d+)/manage-speakers/$',
        views.TalkProposalManageSpeakersView.as_view(),
        name='talk_proposal_manage_speakers'),

    url(r'^tutorial/submit/$',
        views.TutorialProposalCreateView.as_view(),
        name='tutorial_proposal_create'),
    url(r'^talk/(?P<pk>\d+)/peek/$',
        views.ReadonlyTutorialProposalUpdateView.as_view(),
        name='tutorial_proposal_peek'),
    url(r'^tutorial/(?P<pk>\d+)/edit/$',
        views.TutorialProposalUpdateView.as_view(),
        name='tutorial_proposal_update'),
    url(r'^tutorial/(?P<pk>\d+)/cancel/$',
        views.TutorialProposalCancelView.as_view(),
        name='tutorial_proposal_cancel'),
    url(r'^tutorial/(?P<pk>\d+)/manage-speakers/$',
        views.TutorialProposalManageSpeakersView.as_view(),
        name='tutorial_proposal_manage_speakers'),

    url(r'^remove-speaker/(?P<pk>\d+)/$',
        views.AdditionalSpeakerRemoveView.as_view(),
        name='additional_speaker_remove'),
    url(r'^set-speaker-status/(?P<pk>\d+)/$',
        views.AdditionalSpeakerSetStatusView.as_view(),
        name='additional_speaker_set_status'),
]
