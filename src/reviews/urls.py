from django.conf.urls import url

from .views import TalkProposalListView
from .views import ReviewUpdateView, ReviewCreateView


urlpatterns = [
    url(r'^$', TalkProposalListView.as_view(), name='review_proposal_list'),
    url(r'^create/(?P<proposal_pk>\d+)/$',
        ReviewCreateView.as_view(), name='review_create'),
    url(r'^update/(?P<pk>\d+)/$',
        ReviewUpdateView.as_view(), name='review_update'),
]
