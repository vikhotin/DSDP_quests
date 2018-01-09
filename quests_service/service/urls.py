from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^quest/$', views.QuestsView.as_view()),
    url(r'^quest/(?P<quest_id>[0-9]+)/$', views.QuestView.as_view()),
    url(r'^user/(?P<user_id>[0-9]+)/quests/$', views.UserQuestsView.as_view()),
]
