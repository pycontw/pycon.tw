from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^submit/$',
        views.ProposalCreateChoiceView.as_view(),
        name='proposal_create_choice'),

    url(r'^talk/submit/$',
        views.TalkProposalCreateView.as_view(),
        name='talk_proposal_create'),
    url(r'^talk/(?P<pk>\d+)/edit/$',
        views.TalkProposalUpdateView.as_view(),
        name='talk_proposal_update'),
    url(r'^talk/(?P<pk>\d+)/cancel/$',
        views.TalkProposalCancelView.as_view(),
        name='talk_proposal_cancel'),

    url(r'^tutorial/submit/$',
        views.TutorialProposalCreateView.as_view(),
        name='tutorial_proposal_create'),
    url(r'^tutorial/(?P<pk>\d+)/edit/$',
        views.TutorialProposalUpdateView.as_view(),
        name='tutorial_proposal_update'),
    url(r'^tutorial/(?P<pk>\d+)/cancel/$',
        views.TutorialProposalCancelView.as_view(),
        name='tutorial_proposal_cancel'),
]
