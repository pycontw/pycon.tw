from django.conf.urls import url

from .views import ReviewEditView, TalkProposalListView
from . import views

urlpatterns = [
    url(r'^$', TalkProposalListView.as_view(), name='review_proposal_list'),
    url(r'^talk/(?P<proposal_pk>\d+)/$',
        ReviewEditView.as_view(),
        name='review_edit'),
    url(r'^review-stages/$', views.review_stages, name='review_stages'),
]
