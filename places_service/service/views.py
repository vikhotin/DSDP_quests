from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core import serializers
import binascii
import os
from django.utils import timezone

from .models import Place, Fact, Puzzle, Token
from .forms import PlaceForm, FactForm, PuzzleForm


class TokenView(View):
    def get(self, request, *args, **kwargs):
        clientId = request.GET.get('clientId')
        clientSecret = request.GET.get('clientSecret')
        try:
            tok = Token.objects.get(client_id=clientId, client_secret=clientSecret)
        except Token.DoesNotExist:
            return HttpResponse(status=403)
        new_token = binascii.hexlify(os.urandom(15)).decode('ascii')
        tok.token = new_token
        tok.expires = timezone.now() + timezone.timedelta(minutes=30)
        tok.save()
        return JsonResponse({'token': new_token}, safe=False)


def is_token_valid(token):
    try:
        tok = Token.objects.get(token=token)
    except Token.DoesNotExist:
        return False
    if tok.expires < timezone.now():
        return False
    return True


class PlacesView(View):
    http_method_names = ['get', 'post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PlacesView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        place_info = Place.objects.all()
        place_json = serializers.serialize('json', place_info)
        return JsonResponse(place_json, safe=False)

    def post(self, request, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        form = PlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('', status=201)
        else:
            # raise Exception(form.errors)
            return HttpResponse(form.errors, status=400)


class PlaceView(View):
    def get(self, request, place_id, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        try:
            place_info = Place.objects.get(id=place_id)
        except Place.DoesNotExist:
            return HttpResponse('{}', content_type='application/json', status=404)
        place_json = place_info.to_json()
        return JsonResponse(place_json, safe=False)


class FactsView(View):
    http_method_names = ['get', 'post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(FactsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        place_id = kwargs['place_id']
        fact_info = Fact.objects.filter(place=place_id)
        fact_json = serializers.serialize('json', fact_info)
        return JsonResponse(fact_json, safe=False)

    def post(self, request, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        form = FactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('', status=201)
        else:
            # raise Exception(form.errors)
            return HttpResponse(form.errors, status=400)


class FactView(View):
    def get(self, request, fact_id, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        try:
            fact_info = Fact.objects.get(id=fact_id)
        except Fact.DoesNotExist:
            return HttpResponse('{}', content_type='application/json', status=404)
        fact_json = fact_info.to_json()
        return JsonResponse(fact_json, safe=False)


class PuzzlesView(View):
    http_method_names = ['get', 'post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PuzzlesView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        place_id = kwargs['place_id']
        puzzle_info = Puzzle.objects.filter(place=place_id)
        puzzle_json = serializers.serialize('json', puzzle_info)
        return JsonResponse(puzzle_json, safe=False)

    def post(self, request, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        form = PuzzleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('', status=201)
        else:
            # raise Exception(form.errors)
            return HttpResponse(form.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PuzzleView(View):
    def get(self, request, puzzle_id, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        try:
            puzzle_info = Puzzle.objects.get(id=puzzle_id)
        except Puzzle.DoesNotExist:
            return HttpResponse('{}', content_type='application/json', status=404)
        puzzle_json = puzzle_info.to_json()
        return JsonResponse(puzzle_json, safe=False)

    # check if answer is correct
    def post(self, request, puzzle_id, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        try:
            puzzle_info = Puzzle.objects.get(id=puzzle_id)
        except Puzzle.DoesNotExist:
            return HttpResponse('{}', content_type='application/json', status=404)
        if request.POST['answer'] == puzzle_info.answer:
            return JsonResponse({"result": "correct"}, safe=False)
        else:
            return JsonResponse({"result": "wrong"}, safe=False)
