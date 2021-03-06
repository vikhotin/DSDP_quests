from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import requests

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregator.settings')

app = Celery('aggregator')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

user_service_address = 'http://127.0.0.1:8010'
places_service_address = 'http://127.0.0.1:8020'
quests_service_address = 'http://127.0.0.1:8030'


@app.task(bind=True, default_retry_delay=10)
def task_check_user_answer(self, puzzle_id, place_id, quest_id, user_login, user_answer,
                           places_token, places_client, places_secret,
                           quests_token, quests_client, quests_secret):
    try:
        header = {'Authorization': 'Bearer ' + places_token}
        res2 = requests.post(places_service_address + '/place/{}/puzzle/{}/'.format(place_id, puzzle_id),
                             data={'answer': user_answer}, headers=header)
        if res2.status_code == 401:
            res2 = requests.get(places_service_address + '/token/?clientId={}&clientSecret={}'
                                .format(places_client, places_secret), headers=header)
            places_token = res2.json()['token']
            header = {'Authorization': 'Bearer ' + places_token}
            res2 = requests.post(places_service_address + '/place/{}/puzzle/{}/'.format(place_id, puzzle_id),
                                data={'answer': user_answer}, headers=header)

        if res2.json()['result'] != 'correct':
            pass  # todo: tell user he's wrong
        else:
            # todo: tell user he's correct
            header = {'Authorization': 'Bearer ' + quests_token}
            res3 = requests.put(quests_service_address + '/quest/{}/'.format(quest_id),
                                headers=header)
            if res3.status_code == 401:
                res3 = requests.get(quests_service_address + '/token/?clientId={}&clientSecret={}'
                                    .format(quests_client, quests_secret), headers=header)
                quests_token = res3.json()['token']
                header = {'Authorization': 'Bearer ' + quests_token}
                res3 = requests.put(quests_service_address + '/quest/{}/'.format(quest_id),
                                    headers=header)

            if res3.json()['completed'] == 'True':
                task_inc_user_quests_completed.delay(user_login)
    except requests.exceptions.ConnectionError as exc:
        raise self.retry(exc=exc, max_retries=100)


@app.task(bind=True, default_retry_delay=10)
def task_inc_user_quests_completed(self, user_login):
    try:
        res4 = requests.put(user_service_address + '/user/{}/'.format(user_login),
                            {'inc': 'quests_completed'})
    except requests.exceptions.ConnectionError as exc:
        raise self.retry(exc=exc, max_retries=100)
