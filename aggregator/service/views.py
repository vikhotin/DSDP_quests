import requests
import json
import re
from random import shuffle
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

this_service_address = 'http://127.0.0.1:8000'


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
        pass


class UiPlaceInfoView(View):
    # see info about place - some fact
    def get(self, request, *args, **kwargs):
        pass


class UiNewQuestView(View):
    # Create new quest
    def post(self, request, *args, **kwargs):
        pass


class UiUserContributionPuzzle(View):
    # todo in future
    pass


class UiUserContributionFact(View):
    # todo in future
    pass
