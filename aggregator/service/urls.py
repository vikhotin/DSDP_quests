from django.conf.urls import url, include

from . import views


urlpatterns = [
    url('^cur$', views.QuestCurTaskView.as_view()),
]
