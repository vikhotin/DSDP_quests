from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core import serializers

from .models import Quest
from .forms import QuestForm


class QuestsView(View):
    http_method_names = ['get', 'post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(QuestsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        quest_info = Quest.objects.all()
        quest_json = serializers.serialize('json', quest_info)
        return JsonResponse(quest_json, safe=False)

    def post(self, request, *args, **kwargs):
        form = QuestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('', status=201)
        else:
            # raise Exception(form.errors)
            return HttpResponse('', status=409)


class QuestView(View):
    def get(self, request, quest_id, *args, **kwargs):
        try:
            quest_info = Quest.objects.get(id=quest_id)
        except Quest.DoesNotExist:
            return HttpResponse('[]', content_type='application/json', status=404)
        quest_json = quest_info.to_json()
        return JsonResponse(quest_json, safe=False)


class UserQuestsView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id', None)
        if user_id is None:
            return HttpResponse(status=400)
        quest_info = Quest.objects.filter(user_id=user_id)
        if quest_info.exists():
            quest_json = serializers.serialize('json', quest_info)
            return JsonResponse(quest_json, safe=False)
        else:
            return HttpResponse('[]', content_type='application/json', status=404)
