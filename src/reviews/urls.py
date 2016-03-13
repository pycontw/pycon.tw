from django.conf.urls import url

from .views import ReviewEditView, TalkProposalListView


urlpatterns = [
    url(r'^$', TalkProposalListView.as_view(), name='review_proposal_list'),
    url(r'^talk/(?P<proposal_pk>\d+)/$',
        ReviewEditView.as_view(), name='review_edit'),
]
