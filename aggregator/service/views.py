import requests
import json
import re
from random import shuffle
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class UiUserInfoView(View):
    # Get info about user, including his quests list
    def get(self, request, *args, **kwargs):
        pass


class UiUserQuestView(View):
    # Get user's quest - progress
    def get(self, request, *args, **kwargs):
        pass

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
