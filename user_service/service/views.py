from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from pip import status_codes

from .models import User
from .forms import UserForm


class NewUserView(View):
    http_method_names = ['post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(NewUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect('/user/{}/'.format(form.cleaned_data['login']))
            return HttpResponse('', status=201)
        else:
            # raise Exception(form.errors)
            return HttpResponse('', status=409)


class UserView(View):
    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserView, self).dispatch(request, *args, **kwargs)

    def get(self, request, username, *args, **kwargs):
        try:
            User.objects.defer('password')
            user_info = User.objects.get(login=username)
        except User.DoesNotExist:
            return HttpResponse('[]', content_type='application/json', status=404)
        user_json = user_info.to_json()
        return JsonResponse(user_json, safe=False)

    def put(self, request, username, *args, **kwargs):
        if b'quests_number' in request.body:
            user = User.objects.get(login=username)
            user.quests_number += 1
            user.save()
            user_json = user.to_json()
            return JsonResponse(user_json, safe=False)
        elif b'quests_completed' in request.body:
            user = User.objects.get(login=username)
            user.quests_completed += 1
            user.save()
            user_json = user.to_json()
            return JsonResponse(user_json, safe=False)
        else:
            return HttpResponse('', status=400)
