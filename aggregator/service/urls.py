from django.conf.urls import url

from . import views

app_name = 'service'
urlpatterns = [
    # url('^$', views.View.as_view()),
    url('^user/(?P<user_login>.+)/quest/(?P<quest_id>[0-9]+)/place/(?P<place_id>[0-9]+)/fact/(?P<fact_id>[0-9]+)/$',
        views.UiPlaceInfoView.as_view()),
    url('^user/(?P<user_login>.+)/quest/(?P<quest_id>[0-9]+)/$', views.UiUserQuestView.as_view(),
        name='quest'),
    url('^user/(?P<user_login>.+)/quest/$', views.UiNewQuestView.as_view()),
    url('^user/(?P<user_login>.+)/place/(?P<place_id>[0-9]+)/puzzle/$', views.UiUserContributionPuzzle.as_view()),
    url('^user/(?P<user_login>.+)/place/(?P<place_id>[0-9]+)/fact/$', views.UiUserContributionFact.as_view()),
    url('^user/(?P<user_login>.+)/$', views.UiUserInfoView.as_view(), name='user'),
]
