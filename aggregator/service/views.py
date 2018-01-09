import requests
import json
import re
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

user_service_address = 'http://127.0.0.1:8010'
places_service_address = 'http://127.0.0.1:8020'
quests_service_address = 'http://127.0.0.1:8030'


class UserInfoView(View):
    # Get info about user, including his quests list
    @staticmethod
    def get(request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        res = requests.get(user_service_address + '/user/{}/'.format(user_login))
        if res.status_code != 200:
            return HttpResponse(res.text, status=res.status_code)
        user_json = res.json()
        user_id = user_json['id']
        res1 = requests.get(quests_service_address + '/user/{}/quests/'.format(user_id))
        if res1.status_code == 200:
            user_json['quests'] = json.loads(res1.json())
        return JsonResponse(user_json)


@method_decorator(csrf_exempt, name='dispatch')
class UserQuestView(View):
    # Get user's quest - progress
    def get(self, request, *args, **kwargs):
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

        puzzle_id = int(puzzles_ids[cur_task - 1])
        res2 = requests.get(places_service_address + '/puzzle/{}/'.format(puzzle_id))
        if res2.status_code != 200:
            return HttpResponse(res2.text, status=500)

        result = {
            'user': res.json(),
            'quest': res1.json(),
            'puzzle': res2.json(),
        }

        return JsonResponse(result)

    # Post user's answer - check if correct
    def post(self, request, *args, **kwargs):
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
        puzzles_ids = json.loads(quest_json['puzzles_ids'])

        puzzle_id = int(puzzles_ids[cur_task - 1])

        user_answer = request.POST['answer']

        res2 = requests.post(places_service_address + '/puzzle/{}/'.format(puzzle_id),
                             data={'answer': user_answer})
        if res2.status_code != 200:
            return HttpResponse(res2.text, status=500)

        result = {
            'user': res.json(),
            'quest': res1.json(),
            # 'puzzle': res2.json(),
        }
        if res2.json()['result'] != 'correct':
            result['guess'] = 'wrong'
        else:
            result['guess'] = 'correct'
            # TODO: update quest
        return JsonResponse(result)


class PlaceInfoView(View):
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')
        place_id = kwargs.get('place_id')
        fact_id = kwargs.get('fact_id')

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

        puzzle_id = int(puzzles_ids[cur_task - 1])
        res2 = requests.get(places_service_address + '/puzzle/{}/'.format(puzzle_id))
        if res2.status_code != 200:
            return HttpResponse(res2.text, status=500)
        place_from_puzzle = re.findall(r'\d+', res2.json()['place'])[0]

        res3 = requests.get(places_service_address + '/place/{}/'.format(place_id))
        if res3.status_code != 200:
            return HttpResponse(res3.text, status=404)

        res4 = requests.get(places_service_address + '/fact/{}/'.format(fact_id))
        if res4.status_code != 200:
            return HttpResponse(res4.text, status=404)
        place_from_fact = re.findall(r'\d+', res4.json()['place'])[0]

        if not(place_from_puzzle == place_id == place_from_fact):
            return HttpResponse('', status=400)

        result = {
            'user': res.json(),
            'quest': res1.json(),
            'puzzle': res2.json(),
            'place': res3.json(),
            'fact': res4.json(),
        }

        return JsonResponse(result)
