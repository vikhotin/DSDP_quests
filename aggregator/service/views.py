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


class UserQuestView(View):
    # Get user's quest - progress
    @staticmethod
    def get(request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')

        res = requests.get(user_service_address + '/user/{}/'.format(user_login))
        if res.status_code != 200:
            return HttpResponse(res.text, status=res.status_code)
        user_json = res.json()
        user_id = user_json['id']

        res1 = requests.get(quests_service_address + '/quest/{}/'.format(quest_id))
        if res1.status_code != 200:
            return HttpResponse(res1.text, status=res1.status_code)
        quest_json = res1.json()
        quest_user_id = quest_json['user_id']

        if user_id != quest_user_id:
            return HttpResponse("User doesn't have this quest", status=404)

        cur_task = int(quest_json['cur_task'])
        # places_ids = quest_json['places_ids']
        puzzles_ids = json.loads(quest_json['puzzles_ids'])

        puzzle_id = int(puzzles_ids[cur_task-1])
        res2 = requests.get(places_service_address + '/puzzle/{}/'.format(puzzle_id))
        if res2.status_code != 200:
            return HttpResponse(res2.text, status=500)

        result = {
            'user': res.json(),
            'quest': res1.json(),
            'puzzle': res2.json(),
        }

        return JsonResponse(result)
