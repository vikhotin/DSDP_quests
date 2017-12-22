from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.NewUserView.as_view(), name='registration'),
    url(r'^(?P<username>.+)/$', views.UserView.as_view(), name='user'),
]
