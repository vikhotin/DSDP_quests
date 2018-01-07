import requests
import json
from django.http import JsonResponse, HttpResponse
from django.views import View

user_service_address = 'http://127.0.0.1:8010'
places_service_address = 'http://127.0.0.1:8020'
quests_service_address = 'http://127.0.0.1:8030'


class UserInfoView(View):
    # Get info about user, including his quests list
    @staticmethod
    def get(request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        res = requests.get(user_service_address+'/user/{}/'.format(user_login))
        if res.status_code != 200:
            return HttpResponse(res.text, status=res.status_code)
        user_json = res.json()
        user_id = user_json['id']
        res1 = requests.get(quests_service_address+'/user/{}/quests/'.format(user_id))
        if res1.status_code == 200:
            user_json['quests'] = json.loads(res1.json())
        return JsonResponse(user_json)
