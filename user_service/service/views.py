import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import QueryDict
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from django.contrib.auth.models import User
from oauth2_provider.decorators import protected_resource

from .models import MyUser
from .forms import UserForm


@protected_resource()
def check_rights(request):
    return HttpResponse(status=200)


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
            user = User.objects.get(username=form.cleaned_data['username'])
            u = MyUser(user=user)
            u.save()
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
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('{}', content_type='application/json', status=404)
        user_info = MyUser.objects.get(user=user)
        user_json = user_info.to_json()
        return JsonResponse(user_json, safe=False)

    def put(self, request, username, *args, **kwargs):
        user_dj = User.objects.get(username=username)
        user = MyUser.objects.get(user=user_dj)
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

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/login.html', {'client_id': request.GET.get('client_id')})

    def post(self, request, *args, **kwargs):
        login = request.POST.get('login')
        password = request.POST.get('password')
        client_id = request.GET.get('client_id')
        # client_secret = request.GET.get("clientSecret")

        # try:
        #     user_info = MyUser.objects.get(username=login, password=password)
        # except MyUser.DoesNotExist:
        #     return HttpResponse('{}', content_type='application/json', status=404)
        user = authenticate(username=login, password=password)
        if user is not None:
            r = HttpResponseRedirect('http://localhost:8010/o/authorize/?response_type=code&'
                                     'client_id={}&username={}&password={}&'
                                     'redirect_uri=http://localhost:8000/oauth/'.format(
                                         client_id, login, password))
            r.set_cookie('username', login)
            return r
        else:
            return render(request, 'registration/login.html', {'error': 'Неверно введен логин или пароль'})
