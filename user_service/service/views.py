import requests
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import QueryDict
from django.shortcuts import redirect
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
            # raise Exception()
            return HttpResponse(form.errors.as_json(), status=400)


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
            return HttpResponse('{}', content_type='application/json', status=404)
        user_json = user_info.to_json()
        return JsonResponse(user_json, safe=False)

    def put(self, request, username, *args, **kwargs):
        user = User.objects.get(login=username)
        if b'inc' in request.body and b'quests_number' in request.body:
            user.quests_number += 1
            user.save()
            user_json = user.to_json()
            return JsonResponse(user_json, safe=False)
        elif b'inc' in request.body and b'quests_completed' in request.body:
            user.quests_completed += 1
            user.save()
            user_json = user.to_json()
            return JsonResponse(user_json, safe=False)
        elif b'dec' in request.body and b'quests_number' in request.body:
            user.quests_number -= 1
            user.save()
            user_json = user.to_json()
            return JsonResponse(user_json, safe=False)
        elif b'dec' in request.body and b'quests_completed' in request.body:
            user.quests_completed -= 1
            user.save()
            user_json = user.to_json()
            return JsonResponse(user_json, safe=False)
        else:
            return HttpResponse('', status=400)


class LoginView(View):
    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        login = request.POST.get('login')
        password = request.POST.get('password')
        client_id = request.GET.get('clientId')
        client_secret = request.GET.get("clientSecret")

        try:
            user_info = User.objects.get(login=login, password=password)
        except User.DoesNotExist:
            return HttpResponse('{}', content_type='application/json', status=404)

        data = [
            ('grant_type', 'password'),
            ('username', 'admin'),
            ('password', 'adminadmin'),
            ('scope', 'read'),
        ]

        res = requests.post('http://localhost:8010/o/token/', data=data, auth=(client_id, client_secret))

        return HttpResponse(res)
