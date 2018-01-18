import requests
import json
import re
from random import shuffle
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from aggregator.celery import task_check_user_answer

user_service_address = 'http://127.0.0.1:8010'
places_service_address = 'http://127.0.0.1:8020'
quests_service_address = 'http://127.0.0.1:8030'


class ServiceAccess:
    token = ''

    def __init__(self, appId, appSecret):
        self.appId = appId
        self.appSecret = appSecret

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


places_access = ServiceAccess(
    appId='sfFPdNk3trL1CPI42vSx2t4QbCAjgdrn9XyFnmDl',
    appSecret='t2XUiX8SVcx43BzHLlwOExTvUFVEe0GhWlXi1ZMvDhYpKNW0V4s9kr2aqNkY8spcs1SW05pzV5AXVvn0lQRq8oAoM7SgIVcRYi7Sqq1vPVYnSf9de7EH1iOQx1uvdnlH',
)
quests_access = ServiceAccess(
    appId='VLgKe6gqt2grkn0IVRkzWcSATrKkKAup0zbOL2SL',
    appSecret='RSCMdwxOEE1mGAYkp5YxUei6dWm4Py2BLB4bDyLpl4XcP1pm04i5KKCbN8YwTcLdRKEgnWKPDErErWjThmtzy0WI5YaLst0WJJzi7tb0by7r5fUfoXY1KPAVCR87eKbh',
)


def has_access(request):
    header = {'Authorization': 'Bearer ' + str(request.COOKIES.get('access_token'))}
    resp = requests.get(user_service_address + '/user/check_rights/', headers=header)
    if resp.status_code == 200:
        return True
    else:
        return False


def refresh(request):
    res = requests.get('http://127.0.0.1:8000/refresh/', cookies=request.COOKIES)
    if res.status_code == 200:
        return True
    else:
        return False


class UserInfoView(View):
    # Get info about user, including his quests list
    @staticmethod
    def get(request, *args, **kwargs):
        user_login = kwargs.get('user_login')

        if not has_access(request):
            if not refresh(request):
                return HttpResponse('{}', status=401)

        try:
            res = requests.get(user_service_address + '/user/{}/'.format(user_login))
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res.status_code != 200:
            return HttpResponse(res.text, status=res.status_code)

        user_json = res.json()
        user_id = user_json['id']
        page = request.GET.get('page', 0)

        try:
            header = {'Authorization': 'Bearer ' + quests_access.token}
            res1 = requests.get(quests_service_address + '/user/{}/quests/?page={}'.format(user_id, page),
                                headers=header)
            if res1.status_code == 401:
                res1 = requests.get(quests_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(quests_access.appId, quests_access.appSecret), headers=header)
                if res1.status_code == 403:
                    return JsonResponse({'error': 'Access denied'}, status=403)
                else:
                    quests_access.token = res1.json()['token']
                    header = {'Authorization': 'Bearer ' + quests_access.token}
                    res1 = requests.get(quests_service_address + '/user/{}/quests/?page={}'.format(user_id, page),
                                        headers=header)
            if res1.status_code == 200:
                user_json['quests'] = res1.json()['quests']
                user_json['pagination'] = res1.json()['pagination']
        except requests.exceptions.ConnectionError:
            user_json['quests'] = 'Quests currently unavailable'

        return JsonResponse(user_json)


@method_decorator(csrf_exempt, name='dispatch')
class UserQuestView(View):
    # Get user's quest - progress
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')

        if not has_access(request):
            if not refresh(request):
                return HttpResponse('{}', status=401)

        try:
            res = requests.get(user_service_address + '/user/{}/'.format(user_login))
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res.status_code != 200:
            return HttpResponse(res.text, status=res.status_code)
        user_json = res.json()
        user_id = user_json['id']

        try:
            header = {'Authorization': 'Bearer ' + quests_access.token}
            res1 = requests.get(quests_service_address + '/quest/{}/'.format(quest_id),
                                headers=header)
            if res1.status_code == 401:
                res1 = requests.get(quests_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(quests_access.appId, quests_access.appSecret), headers=header)
                if res1.status_code == 403:
                    return JsonResponse({'error': 'Access denied'}, status=403)
                else:
                    quests_access.token = res1.json()['token']
                    header = {'Authorization': 'Bearer ' + quests_access.token}
                    res1 = requests.get(quests_service_address + '/quest/{}/'.format(quest_id),
                                        headers=header)
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res1.status_code != 200:
            return HttpResponse(res1.text, status=res1.status_code)
        quest_json = res1.json()
        quest_user_id = quest_json['user_id']

        if user_id != quest_user_id:
            return HttpResponse('{"error": "User doesn\'t have this quest"}', status=404)

        cur_task = int(quest_json['cur_task'])
        # places_ids = quest_json['places_ids']
        puzzles_ids = json.loads(quest_json['puzzles_ids'])
        places_ids = json.loads(quest_json['places_ids'])

        puzzle_id = int(puzzles_ids[cur_task - 1])
        place_id = int(places_ids[cur_task - 1])
        try:
            header = {'Authorization': 'Bearer ' + places_access.token}
            res2 = requests.get(places_service_address + '/place/{}/puzzle/{}/'.format(place_id, puzzle_id),
                                headers=header)
            if res2.status_code == 401:
                res2 = requests.get(places_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(places_access.appId, places_access.appSecret), headers=header)
                if res2.status_code == 403:
                    return JsonResponse({'error': 'Access denied'}, status=403)
                else:
                    places_access.token = res2.json()['token']
                    header = {'Authorization': 'Bearer ' + places_access.token}
                    res2 = requests.get(places_service_address + '/place/{}/puzzle/{}/'.format(place_id, puzzle_id),
                                        headers=header)
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
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

        if not has_access(request):
            if not refresh(request):
                return HttpResponse('{}', status=401)

        try:
            res = requests.get(user_service_address + '/user/{}/'.format(user_login))
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res.status_code != 200:
            return HttpResponse(res.text, status=res.status_code)
        user_json = res.json()
        user_id = user_json['id']

        try:
            header = {'Authorization': 'Bearer ' + quests_access.token}
            res1 = requests.get(quests_service_address + '/quest/{}/'.format(quest_id),
                                headers=header)
            if res1.status_code == 401:
                res1 = requests.get(quests_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(quests_access.appId, quests_access.appSecret), headers=header)
                if res1.status_code == 403:
                    return JsonResponse({'error': 'Access denied'}, status=403)
                else:
                    quests_access.token = res1.json()['token']
                    header = {'Authorization': 'Bearer ' + quests_access.token}
                    res1 = requests.get(quests_service_address + '/quest/{}/'.format(quest_id),
                                        headers=header)
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res1.status_code != 200:
            return HttpResponse(res1.text, status=res1.status_code)
        quest_json = res1.json()
        quest_user_id = quest_json['user_id']

        if user_id != quest_user_id:
            return HttpResponse('{"error": "User doesn\'t have this quest"}', status=404)

        if quest_json['completed'] == 'True':
            return HttpResponse('{"error": "User has finished this quest"}')

        result = {
            'user': res.json(),
            'quest': res1.json(),
        }

        cur_task = int(quest_json['cur_task'])
        puzzles_ids = json.loads(quest_json['puzzles_ids'])
        places_ids = json.loads(quest_json['places_ids'])

        puzzle_id = int(puzzles_ids[cur_task - 1])
        place_id = int(places_ids[cur_task - 1])

        user_answer = request.POST['answer']

        task_check_user_answer.delay(puzzle_id, place_id, quest_id, user_login, user_answer,
                                     places_access.token, places_access.appId, places_access.appSecret,
                                     quests_access.token, quests_access.appId, quests_access.appSecret)

        result['guess'] = 'checking'

        return JsonResponse(result)


class PlaceInfoView(View):
    # see info about place - some fact
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')
        place_id = kwargs.get('place_id')
        fact_id = kwargs.get('fact_id')

        if not has_access(request):
            if not refresh(request):
                return HttpResponse('{}', status=401)

        try:
            res = requests.get(user_service_address + '/user/{}/'.format(user_login))
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res.status_code != 200:
            return HttpResponse(res.text, status=res.status_code)
        user_json = res.json()
        user_id = user_json['id']

        try:
            header = {'Authorization': 'Bearer ' + quests_access.token}
            res1 = requests.get(quests_service_address + '/quest/{}/'.format(quest_id),
                                headers=header)
            if res1.status_code == 401:
                res1 = requests.get(quests_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(quests_access.appId, quests_access.appSecret), headers=header)
                if res1.status_code == 403:
                    return JsonResponse({'error': 'Access denied'}, status=403)
                else:
                    quests_access.token = res1.json()['token']
                    header = {'Authorization': 'Bearer ' + quests_access.token}
                    res1 = requests.get(quests_service_address + '/quest/{}/'.format(quest_id),
                                        headers=header)
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res1.status_code != 200:
            return HttpResponse(res1.text, status=res1.status_code)
        quest_json = res1.json()
        quest_user_id = quest_json['user_id']

        if user_id != quest_user_id:
            return HttpResponse("User doesn't have this quest", status=404)

        result = {
            'user': res.json(),
            'quest': res1.json(),
        }

        cur_task = int(quest_json['cur_task'])
        # places_ids = quest_json['places_ids']
        puzzles_ids = json.loads(quest_json['puzzles_ids'])

        puzzle_id = int(puzzles_ids[cur_task - 1])
        try:
            header = {'Authorization': 'Bearer ' + places_access.token}
            res2 = requests.get(places_service_address + '/place/{}/puzzle/{}/'.format(place_id, puzzle_id),
                                headers=header)
            if res2.status_code == 401:
                res2 = requests.get(places_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(places_access.appId, places_access.appSecret), headers=header)
                if res2.status_code == 403:
                    return JsonResponse({'error': 'Access denied'}, status=403)
                else:
                    places_access.token = res2.json()['token']
                    header = {'Authorization': 'Bearer ' + places_access.token}
                    res2 = requests.get(places_service_address + '/place/{}/puzzle/{}/'.format(place_id, puzzle_id),
                                        headers=header)
            if res2.status_code != 200:
                return HttpResponse(res2.text, status=500)
            place_from_puzzle = re.findall(r'\d+', res2.json()['place'])[0]

            res3 = requests.get(places_service_address + '/place/{}/'.format(place_id),
                                headers=header)
            if res3.status_code == 401:
                res3 = requests.get(places_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(places_access.appId, places_access.appSecret), headers=header)
                if res3.status_code == 403:
                    return JsonResponse({'error': 'Access denied'}, status=403)
                else:
                    places_access.token = res3.json()['token']
                    header = {'Authorization': 'Bearer ' + places_access.token}
                    res3 = requests.get(places_service_address + '/place/{}/'.format(place_id),
                                        headers=header)
            if res3.status_code != 200:
                return HttpResponse(res3.text, status=404)

            res4 = requests.get(places_service_address + '/place/{}/fact/{}/'.format(place_id, fact_id),
                                headers=header)
            if res4.status_code == 401:
                res4 = requests.get(places_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(places_access.appId, places_access.appSecret), headers=header)
                if res4.status_code == 403:
                    return JsonResponse({'error': 'Access denied'}, status=403)
                else:
                    places_access.token = res4.json()['token']
                    header = {'Authorization': 'Bearer ' + places_access.token}
                    res4 = requests.get(places_service_address + '/place/{}/fact/{}/'.format(place_id, fact_id),
                                        headers=header)
            if res4.status_code != 200:
                return HttpResponse(res4.text, status=404)
            place_from_fact = re.findall(r'\d+', res4.json()['place'])[0]

            if not (place_from_puzzle == place_id == place_from_fact):
                return HttpResponse('', status=400)
        except requests.exceptions.ConnectionError:
            result['puzzle'] = 'Unknown'
            result['place'] = 'Unknown'
            result['fact'] = 'Unknown'
        else:
            result['puzzle'] = res2.json()
            result['place'] = res3.json()
            result['fact'] = res4.json()

        return JsonResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class NewQuestView(View):
    http_method_names = ['post']

    # Create new quest
    def post(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')

        if not has_access(request):
            if not refresh(request):
                return HttpResponse('{}', status=401)

        try:
            res = requests.get(user_service_address + '/user/{}/'.format(user_login))
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res.status_code != 200:
            return HttpResponse(res.text, status=res.status_code)
        user_json = res.json()
        user_id = user_json['id']

        try:
            header = {'Authorization': 'Bearer ' + places_access.token}
            res2 = requests.get(places_service_address + '/place/', headers=header)
            if res2.status_code == 401:
                res2 = requests.get(places_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(places_access.appId, places_access.appSecret), headers=header)
                if res2.status_code == 403:
                    return JsonResponse({'error': 'Access denied'}, status=403)
                else:
                    places_access.token = res2.json()['token']
                    header = {'Authorization': 'Bearer ' + places_access.token}
                    res2 = requests.get(places_service_address + '/place/', headers=header)
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res2.status_code != 200:
            return HttpResponse(res2.text, status=res2.status_code)

        places_json = res2.json()
        places_ids = [i['pk'] for i in json.loads(places_json)]
        shuffle(places_ids)

        puzzles_ids = []
        for i in places_ids:
            try:
                header = {'Authorization': 'Bearer ' + places_access.token}
                # TODO: random puzzle
                resp = requests.get(places_service_address + '/place/{}/puzzle/{}/'.format(i, 1),
                                    headers=header)
                if resp.status_code == 401:
                    resp = requests.get(places_service_address + '/token/?clientId={}&clientSecret={}'
                                        .format(places_access.appId, places_access.appSecret), headers=header)
                    if resp.status_code == 403:
                        return JsonResponse({'error': 'Access denied'}, status=403)
                    else:
                        places_access.token = resp.json()['token']
                        header = {'Authorization': 'Bearer ' + places_access.token}
                        resp = requests.get(places_service_address + '/place/{}/puzzle/{}/'.format(i, 1),
                                            headers=header)
            except requests.exceptions.ConnectionError:
                return JsonResponse({'error': 'Service currently unavailable'}, status=503)
            puzzles_ids.extend([int(resp.json()['id'])])

        # adding the quest
        # increase number of user's quests
        try:
            res3 = requests.put(user_service_address + '/user/{}/'.format(user_login),
                                {'inc': 'quests_number'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Service currently unavailable'}, status=503)
        if res3.status_code != 200:
            return HttpResponse(res3.text, status=res3.status_code)
        else:
            try:
                data = {
                    "user_id": str(user_id),
                    "places_ids": str(places_ids)[1:-1],
                    "puzzles_ids": str(puzzles_ids)[1:-1],
                    "cur_task": str(1),
                    "completed": "False",
                }
                header = {'Authorization': 'Bearer ' + quests_access.token}
                res1 = requests.post(quests_service_address + '/quest/', data, headers=header)
                if res1.status_code == 401:
                    res1 = requests.get(quests_service_address + '/token/?clientId={}&clientSecret={}'
                                        .format(quests_access.appId, quests_access.appSecret), headers=header)
                    if res1.status_code == 403:
                        return JsonResponse({'error': 'Access denied'}, status=403)
                    else:
                        quests_access.token = res1.json()['token']
                        header = {'Authorization': 'Bearer ' + quests_access.token}
                        res1 = requests.post(quests_service_address + '/quest/', data, headers=header)
                if res1.status_code != 201:
                    return HttpResponse(res1.text, status=res1.status_code)
                else:
                    return HttpResponse(status=201)
            except requests.exceptions.ConnectionError:
                # rollback
                try:
                    res3 = requests.put(user_service_address + '/user/{}/'.format(user_login),
                                        {'dec': 'quests_number'})
                except requests.exceptions.ConnectionError:
                    return HttpResponse('{"error": "Fatal error: data might be inconsistent"}', status=503)
                if res3.status_code != 200:
                    return HttpResponse(res3.text, status=res3.status_code)
                else:
                    return HttpResponse('{"error": "Quest currently cannot be added due to a server problem. '
                                        'Try again later"}', status=503)


class UserContributionPuzzle(View):
    # todo in future
    pass


class UserContributionFact(View):
    # todo in future
    pass
