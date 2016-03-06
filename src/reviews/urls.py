from django.conf.urls import url

from .views import TalkProposalDetailView, TalkProposalListView
from .views import ReviewUpdateView


urlpatterns = [
    url(r'^$', TalkProposalListView.as_view(), name='review_proposal_list', ),
    url(r'^proposal/(?P<pk>(\d+))/$', TalkProposalDetailView.as_view(), name='review_proposal_detail', ),
    url(r'^update/(?P<pk>(\d+))/$', ReviewUpdateView.as_view(), name='review_update', ),
]
