import requests
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

this_service_address = 'http://127.0.0.1:8000'

user_service_address = 'http://127.0.0.1:8010'

client_id = 'we3iHS6Z8cfj7CDypvBLhNDtQHrsgjS1HSw5CGFm'
client_secret = 'KyIeQtuXyN2Vc4VMSTAXzuoNebNnk6UAWkcekE5P9wscnPM2EAa0TyZxSZDWc6PH6A179t3fDNXdICLUsBooXF4gmmRqWjixf6pvy3imF6bz3GuEHj9sXDKnjHMrOb8S'


class UiUserInfoView(View):
    # Get info about user, including his quests list
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        page = request.GET.get('page', 1)
        res = requests.get(this_service_address + '/api/user/{}/?page={}'.format(user_login, page))
        data = res.json()
        if res.status_code == 200:
            return render(request, 'service/userinfo.html', data)
        elif res.status_code == 404:
            return render(request, 'service/404.html', data)
        elif res.status_code == 503:
            return render(request, 'service/503.html', data)
        else:
            return res


class UiUserQuestView(View):
    # Get user's quest - progress
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')
        res = requests.get(this_service_address + '/api/user/{}/quest/{}/'.format(user_login, quest_id))
        data = res.json()
        if res.status_code == 200:
            return render(request, 'service/questinfo.html', data)
        elif res.status_code == 404:
            return render(request, 'service/404.html', data)
        elif res.status_code == 503:
            return render(request, 'service/503.html', data)
        else:
            return res

    # Post user's answer - check if correct
    def post(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')
        answer = request.POST.get('answer')
        res = requests.post(this_service_address + '/api/user/{}/quest/{}/'.format(user_login, quest_id),
                            data={'answer': answer})
        data = res.json()
        if res.status_code == 200:
            return render(request, 'service/questinfo.html', data)
        elif res.status_code == 404:
            return render(request, 'service/404.html', data)
        elif res.status_code == 503:
            return render(request, 'service/503.html', data)
        else:
            return res


class UiPlaceInfoView(View):
    # see info about place - some fact
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')
        place_id = kwargs.get('place_id')
        fact_id = kwargs.get('fact_id')
        res = requests.get(this_service_address + '/api/user/{}/quest/{}/place/{}/fact/{}/'.format(
            user_login, quest_id, place_id, fact_id))
        data = res.json()
        if res.status_code == 200:
            return render(request, 'service/placefact.html', data)
        elif res.status_code == 404:
            return render(request, 'service/404.html', data)
        elif res.status_code == 503:
            return render(request, 'service/503.html', data)
        else:
            return res


class UiNewQuestView(View):
    # Create new quest
    def post(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        res = requests.post(this_service_address + '/api/user/{}/quest/'.format(user_login))
        if res.status_code == 201:
            return redirect('service:user', user_login)
        elif res.status_code == 404:
            data = res.json()
            return render(request, 'service/404.html', data)
        elif res.status_code == 503:
            data = res.json()
            return render(request, 'service/503.html', data)
        else:
            return res


class UiUserContributionPuzzle(View):
    # todo in future
    pass


class UiUserContributionFact(View):
    # todo in future
    pass


class UiIndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'service/index.html')


class UiLoginView(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'service/login.html')
        return HttpResponseRedirect('http://localhost:8010/o/authorize/?response_type=code&'
                                    'client_id={}&redirect_uri=http://localhost:8000/oauth/'.format(
                                        client_id))

    def post(self, request, *args, **kwargs):
        pass
        '''
        try:
            res = requests.post(user_service_address + '/user/login/?clientId={}&clientSecret={}'
                                .format(clientId, clientSecret), request.POST)
        except requests.exceptions.ConnectionError:
            return render(request, 'service/login.html', {'error': 'Service currently unavailable'}, status=503)

        if res.status_code == 404:
            return render(request, 'service/login.html', {'error': 'Неверно введен логин или пароль'})
        else:
            # redo
            return HttpResponse(res)
        '''


@method_decorator(csrf_exempt, name='dispatch')
class AuthView(View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        try:
            res = requests.post('http://localhost:8010/o/token/',
                                {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': 'http://localhost:8000/oauth/'}, auth=(client_id, client_secret))
        except requests.exceptions.ConnectionError:
            data = res.json()
            return render(request, 'service/503.html', data)
        if res.status_code != 200:
            return res

        username = request.COOKIES.get('username')
        res1 = HttpResponseRedirect(reverse('service:user', args=[username]))
        # res1 = HttpResponse()
        res1.set_cookie('access_token', res.json()['access_token'])
        res1.set_cookie('refresh_token', res.json()['refresh_token'])

        return res1
