from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^place/$', views.PlacesView.as_view()),
    url(r'^place/(?P<place_id>[0-9]+)/$', views.PlaceView.as_view()),

]
