from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core import serializers
from django.core.paginator import Paginator
from json import loads
import binascii
import os
from django.utils import timezone

from .models import Quest, Token
from .forms import QuestForm


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


class QuestsView(View):
    http_method_names = ['get', 'post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(QuestsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        quest_info = Quest.objects.all()
        quest_json = serializers.serialize('json', quest_info)
        return JsonResponse(quest_json, safe=False)

    def post(self, request, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        form = QuestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('', status=201)
        else:
            # raise Exception(form.errors)
            return HttpResponse(form.errors.as_json(), status=400)


class QuestView(View):
    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(QuestView, self).dispatch(request, *args, **kwargs)

    def get(self, request, quest_id, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        try:
            quest_info = Quest.objects.get(id=quest_id)
        except Quest.DoesNotExist:
            return HttpResponse('{}', content_type='application/json', status=404)
        quest_json = quest_info.to_json()
        return JsonResponse(quest_json, safe=False)

    def put(self, request, quest_id, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        try:
            q = Quest.objects.get(id=quest_id)
            if q.cur_task == len(q.places_ids):
                q.completed = True
            else:
                q.cur_task += 1
            q.save()
            user_json = q.to_json()
            return JsonResponse(user_json, safe=False)
        except Quest.DoesNotExist:
            return HttpResponse('', status=500)


class UserQuestsView(View):
    def get(self, request, *args, **kwargs):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if not is_token_valid(token):
            return HttpResponse('', status=401)
        page_size = 5
        user_id = kwargs.get('user_id', None)
        if user_id is None:
            return HttpResponse(status=400)
        quest_info = Quest.objects.filter(user_id=user_id).order_by('id')
        if quest_info.exists():
            pag = Paginator(quest_info, page_size)
            page = request.GET.get('page', 1)
            quest_page = pag.get_page(page)
            quest_json = serializers.serialize('json', quest_page)
            quest_json = loads(quest_json)
            quest_json = {
                'pagination': {
                    'has_previous': quest_page.has_previous(),
                    'previous_page_number': quest_page.previous_page_number() if quest_page.has_previous() else '',
                    'number': quest_page.number,
                    'num_pages': quest_page.paginator.num_pages,
                    'has_next': quest_page.has_next(),
                    'next_page_number': quest_page.next_page_number() if quest_page.has_next() else '',
                },
                'quests': quest_json
            }
            return JsonResponse(quest_json, safe=False)
        else:
            return HttpResponse('{}', content_type='application/json', status=404)
