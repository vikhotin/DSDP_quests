from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^place/$', views.PlacesView.as_view()),
    url(r'^place/(?P<place_id>[0-9]+)/$', views.PlaceView.as_view()),

    url(r'^place/(?P<place_id>[0-9]+)/fact/$', views.FactsView.as_view()),
    url(r'^place/(?P<place_id>[0-9]+)/fact/(?P<fact_id>[0-9]+)/$', views.FactView.as_view()),

    url(r'^place/(?P<place_id>[0-9]+)/puzzle/$', views.PuzzlesView.as_view()),
    url(r'^place/(?P<place_id>[0-9]+)/puzzle/(?P<puzzle_id>[0-9]+)/$', views.PuzzleView.as_view()),
]
