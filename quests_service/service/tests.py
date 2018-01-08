from django.test import TestCase
from .models import Quest


class QuestViewTests(TestCase):
    def setUp(self):
        quest = Quest.objects.create(user_id=1, places_ids=[1, 2], puzzles_ids=[1, 1], cur_task=1, completed=0)
        self.id = quest.id

    def test_get_quest_ok(self):
        response = self.client.get('/quest/{}/'.format(self.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1')
        self.assertContains(response, '2')

    def test_get_quest_not_exist(self):
        response = self.client.get('/quest/1000/')
        self.assertEqual(response.status_code, 404)


class QuestsViewTests(TestCase):
    def setUp(self):
        Quest.objects.create(user_id=1, places_ids=[11, 12], puzzles_ids=[1, 1], cur_task=1, completed=0)
        Quest.objects.create(user_id=2, places_ids=[13, 14], puzzles_ids=[1, 1], cur_task=1, completed=0)

    def test_get_quests_ok(self):
        response = self.client.get('/quest/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '11')
        self.assertContains(response, '12')
        self.assertContains(response, '13')
        self.assertContains(response, '14')

    def test_post_quest(self):
        response = self.client.post('/quest/', {'user_id': '2', 'places_ids': '1, 2', 'puzzles_ids': '1, 1',
                                                'cur_task': '1', 'completed': '0'})
        self.assertEqual(response.status_code, 201)

    def test_post_quest_invalid(self):
        response = self.client.post('/quest/', {'user_id': '2', 'places_ids': '[wrong, wrong]', 'puzzles_ids': '1, 1',
                                                'cur_task': '1', 'completed': '0'})
        self.assertEqual(response.status_code, 409)


class UserQuestsViewTests(TestCase):
    def setUp(self):
        Quest.objects.create(user_id=1, places_ids=[11, 12], puzzles_ids=[1, 1], cur_task=1, completed=0)
        Quest.objects.create(user_id=2, places_ids=[13, 14], puzzles_ids=[1, 1], cur_task=1, completed=0)

    def test_get_quests_ok(self):
        response = self.client.get('/user/1/quests/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '11')
        self.assertContains(response, '12')
        self.assertNotContains(response, '13')
        self.assertNotContains(response, '14')

    def test_get_quests_not_exists(self):
        response = self.client.get('/user/21/quests/')
        self.assertEqual(response.status_code, 404)
