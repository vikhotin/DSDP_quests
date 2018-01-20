from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.NewUserView.as_view(), name='registration'),
    url(r'^check_rights/$', views.check_rights, name='check'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^token_check/$', views.TokenCheckView.as_view()),
    url(r'^token/$', views.TokenView.as_view()),
    url(r'^(?P<username>.+)/$', views.UserView.as_view(), name='user'),
]
