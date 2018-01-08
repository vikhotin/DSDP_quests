from django.conf.urls import url

from . import views


urlpatterns = [
    # url('^$', views.View.as_view()),
    url('^user/(?P<user_login>.+)/quest/(?P<quest_id>[0-9]+)/$', views.UserQuestView.as_view()),
    url('^user/(?P<user_login>.+)/$', views.UserInfoView.as_view()),
]
