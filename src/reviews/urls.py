from django.conf.urls import url

from .views import TalkProposalDetailView, TalkProposalListView


urlpatterns = [
    url(r'^$', TalkProposalListView.as_view(), name='review_proposal_list', ),
    url(r'^(?P<pk>(\d+))/$', TalkProposalDetailView.as_view(), name='review_proposal_detail', ),
]
