from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core import serializers

from .models import Place, Fact, Puzzle
from .forms import PlaceForm, FactForm, PuzzleForm


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


class FactsView(View):
    http_method_names = ['get', 'post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(FactsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        fact_info = Fact.objects.all()
        fact_json = serializers.serialize('json', fact_info)
        return JsonResponse(fact_json, safe=False)

    def post(self, request, *args, **kwargs):
        form = FactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('', status=201)
        else:
            raise Exception(form.errors)
            # return HttpResponse('', status=409)


class FactView(View):
    def get(self, request, fact_id, *args, **kwargs):
        try:
            fact_info = Fact.objects.get(id=fact_id)
        except Fact.DoesNotExist:
            return HttpResponse('[]', content_type='application/json', status=404)
        fact_json = fact_info.to_json()
        return JsonResponse(fact_json, safe=False)


class PuzzlesView(View):
    http_method_names = ['get', 'post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PuzzlesView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        puzzle_info = Puzzle.objects.all()
        puzzle_json = serializers.serialize('json', puzzle_info)
        return JsonResponse(puzzle_json, safe=False)

    def post(self, request, *args, **kwargs):
        form = PuzzleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('', status=201)
        else:
            raise Exception(form.errors)
            # return HttpResponse('', status=409)


@method_decorator(csrf_exempt, name='dispatch')
class PuzzleView(View):
    def get(self, request, puzzle_id, *args, **kwargs):
        try:
            puzzle_info = Puzzle.objects.get(id=puzzle_id)
        except Puzzle.DoesNotExist:
            return HttpResponse('[]', content_type='application/json', status=404)
        puzzle_json = puzzle_info.to_json()
        return JsonResponse(puzzle_json, safe=False)

    # check if answer is correct
    def post(self, request, puzzle_id, *args, **kwargs):
        try:
            puzzle_info = Puzzle.objects.get(id=puzzle_id)
        except Puzzle.DoesNotExist:
            return HttpResponse('[]', content_type='application/json', status=404)
        if request.POST['answer'] == puzzle_info.answer:
            return JsonResponse({"result": "correct"}, safe=False)
        else:
            return JsonResponse({"result": "wrong"}, safe=False)
