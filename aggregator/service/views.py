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

        data = {
            'username': user_login,
            'token': request.COOKIES['uid_token']
        }
        res = requests.post('http://localhost:8010/user/token_check/', data=data)
        if res.status_code == 401:
            return HttpResponseRedirect(reverse('service:index'))

        res = requests.get(this_service_address + '/api/user/{}/?page={}'.format(user_login, page),
                           cookies=request.COOKIES)
        if res.status_code == 401:
            res = requests.get('http://127.0.0.1:8000/refresh/', cookies=request.COOKIES)
            if res.status_code != 200:
                return HttpResponseRedirect('http://127.0.0.1:8000/')
            request.COOKIES['access_token'] = res.cookies.get('access_token')
            request.COOKIES['refresh_token'] = res.cookies.get('refresh_token')
            res = requests.get(this_service_address + '/api/user/{}/?page={}'.format(user_login, page),
                               cookies=request.COOKIES)
            if res.status_code == 401:
                return HttpResponseRedirect('http://127.0.0.1:8000/')

        data = res.json()

        if res.status_code == 200:
            result = render(request, 'service/userinfo.html', data)
        elif res.status_code == 404:
            result = render(request, 'service/404.html', data)
        elif res.status_code == 403:
            result = render(request, 'service/403.html', data)
        elif res.status_code == 503:
            result = render(request, 'service/503.html', data)
        else:
            result = res

        result.set_cookie('access_token', request.COOKIES['access_token'])
        result.set_cookie('refresh_token', request.COOKIES['refresh_token'])

        return result


class UiUserQuestView(View):
    # Get user's quest - progress
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')

        data = {
            'username': user_login,
            'token': request.COOKIES['uid_token']
        }
        res = requests.post('http://localhost:8010/user/token_check/', data=data)
        if res.status_code == 401:
            return HttpResponseRedirect(reverse('service:index'))

        res = requests.get(this_service_address + '/api/user/{}/quest/{}/'.format(user_login, quest_id),
                           cookies=request.COOKIES)
        if res.status_code == 401:
            res = requests.get('http://127.0.0.1:8000/refresh/', cookies=request.COOKIES)
            if res.status_code != 200:
                return HttpResponseRedirect('http://127.0.0.1:8000/')
            request.COOKIES['access_token'] = res.cookies.get('access_token')
            request.COOKIES['refresh_token'] = res.cookies.get('refresh_token')
            res = requests.get(this_service_address + '/api/user/{}/quest/{}/'.format(user_login, quest_id),
                               cookies=request.COOKIES)
            if res.status_code == 401:
                return HttpResponseRedirect('http://127.0.0.1:8000/')

        data = res.json()
        if res.status_code == 200:
            result = render(request, 'service/questinfo.html', data)
        elif res.status_code == 404:
            result = render(request, 'service/404.html', data)
        elif res.status_code == 503:
            result = render(request, 'service/503.html', data)
        else:
            result = res

        result.set_cookie('access_token', request.COOKIES['access_token'])
        result.set_cookie('refresh_token', request.COOKIES['refresh_token'])

        return result

    # Post user's answer - check if correct
    def post(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')
        answer = request.POST.get('answer')

        data = {
            'username': user_login,
            'token': request.COOKIES['uid_token']
        }
        res = requests.post('http://localhost:8010/user/token_check/', data=data)
        if res.status_code == 401:
            return HttpResponseRedirect(reverse('service:index'))

        res = requests.post(this_service_address + '/api/user/{}/quest/{}/'.format(user_login, quest_id),
                            data={'answer': answer},
                            cookies=request.COOKIES)
        if res.status_code == 401:
            res = requests.get('http://127.0.0.1:8000/refresh/', cookies=request.COOKIES)
            if res.status_code != 200:
                return HttpResponseRedirect('http://127.0.0.1:8000/')
            request.COOKIES['access_token'] = res.cookies.get('access_token')
            request.COOKIES['refresh_token'] = res.cookies.get('refresh_token')
            res = requests.post(this_service_address + '/api/user/{}/quest/{}/'.format(user_login, quest_id),
                                data={'answer': answer},
                                cookies=request.COOKIES)
            if res.status_code == 401:
                return HttpResponseRedirect('http://127.0.0.1:8000/')

        data = res.json()
        if res.status_code == 200:
            result = render(request, 'service/questinfo.html', data)
        elif res.status_code == 404:
            result = render(request, 'service/404.html', data)
        elif res.status_code == 503:
            result = render(request, 'service/503.html', data)
        else:
            result = res

        result.set_cookie('access_token', request.COOKIES['access_token'])
        result.set_cookie('refresh_token', request.COOKIES['refresh_token'])

        return result


class UiPlaceInfoView(View):
    # see info about place - some fact
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')
        place_id = kwargs.get('place_id')
        fact_id = kwargs.get('fact_id')

        data = {
            'username': user_login,
            'token': request.COOKIES['uid_token']
        }
        res = requests.post('http://localhost:8010/user/token_check/', data=data)
        if res.status_code == 401:
            return HttpResponseRedirect(reverse('service:index'))

        res = requests.get(this_service_address + '/api/user/{}/quest/{}/place/{}/fact/{}/'.format(
            user_login, quest_id, place_id, fact_id), cookies=request.COOKIES)
        if res.status_code == 401:
            res = requests.get('http://127.0.0.1:8000/refresh/', cookies=request.COOKIES)
            if res.status_code != 200:
                return HttpResponseRedirect('http://127.0.0.1:8000/')
            request.COOKIES['access_token'] = res.cookies.get('access_token')
            request.COOKIES['refresh_token'] = res.cookies.get('refresh_token')
            res = requests.get(this_service_address + '/api/user/{}/quest/{}/place/{}/fact/{}/'.format(
                user_login, quest_id, place_id, fact_id), cookies=request.COOKIES)
            if res.status_code == 401:
                return HttpResponseRedirect('http://127.0.0.1:8000/')
        data = res.json()
        if res.status_code == 200:
            result = render(request, 'service/placefact.html', data)
        elif res.status_code == 404:
            result = render(request, 'service/404.html', data)
        elif res.status_code == 503:
            result = render(request, 'service/503.html', data)
        else:
            result = res

        result.set_cookie('access_token', request.COOKIES['access_token'])
        result.set_cookie('refresh_token', request.COOKIES['refresh_token'])

        return result


class UiNewQuestView(View):
    # Create new quest
    def post(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')

        data = {
            'username': user_login,
            'token': request.COOKIES['uid_token']
        }
        res = requests.post('http://localhost:8010/user/token_check/', data=data)
        if res.status_code == 401:
            return HttpResponseRedirect(reverse('service:index'))

        res = requests.post(this_service_address + '/api/user/{}/quest/'.format(user_login),
                            cookies=request.COOKIES)
        if res.status_code == 401:
            res = requests.get('http://127.0.0.1:8000/refresh/', cookies=request.COOKIES)
            if res.status_code != 200:
                return HttpResponseRedirect('http://127.0.0.1:8000/')
            request.COOKIES['access_token'] = res.cookies.get('access_token')
            request.COOKIES['refresh_token'] = res.cookies.get('refresh_token')
            res = requests.post(this_service_address + '/api/user/{}/quest/'.format(user_login),
                                cookies=request.COOKIES)
        if res.status_code == 401:
            result = HttpResponseRedirect('http://127.0.0.1:8000/')
        if res.status_code == 201:
            result = redirect('service:user', user_login)
        elif res.status_code == 404:
            data = res.json()
            result = render(request, 'service/404.html', data)
        elif res.status_code == 503:
            data = res.json()
            result = render(request, 'service/503.html', data)
        else:
            result = res

        result.set_cookie('access_token', request.COOKIES['access_token'])
        result.set_cookie('refresh_token', request.COOKIES['refresh_token'])

        return result


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
        return render(request, 'service/login.html')

    def post(self, request, *args, **kwargs):
        data = {
            "username": request.POST['login'],
            "password": request.POST['password'],
        }
        res = requests.post('http://localhost:8010/user/token/', data=data)
        if res.status_code == 403:
            return render(request, 'service/login.html', {'error': 'Неверный логин или пароль'})
        else:
            resp = render(request, 'service/login_ok.html')
            resp.set_cookie('uid_token', res.json()['token'])
            return resp


class ApiLoginView(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'service/login.html')
        return HttpResponseRedirect('http://localhost:8010/o/authorize/?response_type=code&'
                                    'client_id={}&redirect_uri=http://localhost:8000/oauth/'.format(
                                        client_id))

    def post(self, request, *args, **kwargs):
        pass


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


@method_decorator(csrf_exempt, name='dispatch')
class RefreshView(View):
    def get(self, request, *args, **kwargs):
        try:
            res = requests.post('http://localhost:8010/o/token/?grant_type=refresh_token&client_id={}&'
                                'client_secret={}&refresh_token={}&redirect_uri=http://localhost:8000/oauth/'.format(
                                    client_id, client_secret, request.COOKIES['refresh_token']))
            # res = requests.post('http://localhost:8010/o/token/',
            #                     {'grant_type': 'refresh_token', 'refresh_token': request.COOKIES['refresh_token'],
            #                      'redirect_uri': 'http://localhost:8000/oauth/'}, auth=(client_id, client_secret))
        except requests.exceptions.ConnectionError:
            data = res.json()
            return render(request, 'service/503.html', data)
        if res.status_code != 200:
            return res

        res1 = HttpResponse()
        res1.set_cookie('access_token', res.json()['access_token'])
        res1.set_cookie('refresh_token', res.json()['refresh_token'])

        return res1
