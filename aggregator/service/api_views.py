import requests
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .service_methods import GetUserInfo, GetUserQuestInfo, PostUserQuest, GetPlaceInfo, PostNewQuest

user_service_address = 'http://127.0.0.1:8010'


def has_access(request):
    header = {'Authorization': 'Bearer ' + str(request.COOKIES.get('access_token'))}
    resp = requests.get(user_service_address + '/user/check_rights/', headers=header)
    if resp.status_code == 200:
        return True
    else:
        return False


class UserInfoView(View):
    # Get info about user, including his quests list
    @staticmethod
    def get(request, *args, **kwargs):
        user_login = kwargs.get('user_login')

        if not has_access(request):
            return HttpResponse('{}', status=401)

        return GetUserInfo(request, user_login)


@method_decorator(csrf_exempt, name='dispatch')
class UserQuestView(View):
    # Get user's quest - progress
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')

        if not has_access(request):
            return HttpResponse('{}', status=401)

        return GetUserQuestInfo(quest_id, user_login)

    # Post user's answer - check if correct
    def post(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')

        if not has_access(request):
            return HttpResponse('{}', status=401)

        return PostUserQuest(quest_id, request, user_login)


class PlaceInfoView(View):
    # see info about place - some fact
    def get(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')
        quest_id = kwargs.get('quest_id')
        place_id = kwargs.get('place_id')
        fact_id = kwargs.get('fact_id')

        if not has_access(request):
            return HttpResponse('{}', status=401)

        return GetPlaceInfo(fact_id, place_id, quest_id, user_login)


@method_decorator(csrf_exempt, name='dispatch')
class NewQuestView(View):
    http_method_names = ['post']

    # Create new quest
    def post(self, request, *args, **kwargs):
        user_login = kwargs.get('user_login')

        if not has_access(request):
            return HttpResponse('{}', status=401)

        return PostNewQuest(user_login)


class UserContributionPuzzle(View):
    # todo in future
    pass


class UserContributionFact(View):
    # todo in future
    pass
