from django.conf.urls import url

from . import api_views


urlpatterns = [
    # url('^$', views.View.as_view()),
    url('^user/(?P<user_login>.+)/quest/(?P<quest_id>[0-9]+)/place/(?P<place_id>[0-9]+)/fact/(?P<fact_id>[0-9]+)/$',
        api_views.PlaceInfoView.as_view()),
    url('^user/(?P<user_login>.+)/quest/(?P<quest_id>[0-9]+)/$', api_views.UserQuestView.as_view()),
    url('^user/(?P<user_login>.+)/quest/$', api_views.NewQuestView.as_view()),
    url('^user/(?P<user_login>.+)/place/(?P<place_id>[0-9]+)/puzzle/$', api_views.UserContributionPuzzle.as_view()),
    url('^user/(?P<user_login>.+)/place/(?P<place_id>[0-9]+)/fact/$', api_views.UserContributionFact.as_view()),
    url('^user/(?P<user_login>.+)/$', api_views.UserInfoView.as_view()),
]
