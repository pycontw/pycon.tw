from django.conf.urls import url

from .views import TalkProposalDetailView, TalkProposalListView


urlpatterns = [
    url(r'^$', TalkProposalListView.as_view(), name='proposal-list', ),
    url(r'^(?P<pk>(\d+))/$', TalkProposalDetailView.as_view(), name='proposal-detail', ),
]
