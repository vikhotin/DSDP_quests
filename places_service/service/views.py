from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core import serializers

from .models import Place, Fact, Puzzle
from .forms import PlaceForm


class PlacesView(View):
    http_method_names = ['get', 'post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PlacesView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        place_info = Place.objects.all()
        place_json = serializers.serialize('json', place_info)
        return JsonResponse(place_json, safe=False)

    def post(self, request, *args, **kwargs):
        form = PlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('', status=201)
        else:
            # raise Exception(form.errors)
            return HttpResponse('', status=409)


class PlaceView(View):
    def get(self, request, place_id, *args, **kwargs):
        try:
            place_info = Place.objects.get(id=place_id)
        except Place.DoesNotExist:
            return HttpResponse('[]', content_type='application/json', status=404)
        place_json = place_info.to_json()
        return JsonResponse(place_json, safe=False)

