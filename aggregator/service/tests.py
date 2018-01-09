from django.test import TestCase


class UserInfoViewTest(TestCase):
    def test_get_user_info_ok(self):
        response = self.client.get('/user/{}/'.format('user1'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'User User')
        self.assertContains(response, 'fields')

    def test_get_user_info_ok_no_quests(self):
        response = self.client.get('/user/{}/'.format('user2'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user2')
        self.assertContains(response, 'User_ka')
        self.assertNotContains(response, 'fields')

    def test_get_user_info_not_ok(self):
        response = self.client.get('/user/{}/'.format('chupachups'))
        self.assertEqual(response.status_code, 404)


class UserQuestViewTest(TestCase):
    def test_get_user_info_ok(self):
        response = self.client.get('/user/{}/quest/{}/'.format('user1', '1'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'User User')
        self.assertContains(response, 'puzzle')
        self.assertContains(response, 'quest')
        self.assertContains(response, 'places_ids')

    def test_get_user_no_such_quest(self):
        response = self.client.get('/user/{}/quest/{}/'.format('user1', '0'))
        self.assertEqual(response.status_code, 404)

    def test_get_user_not_his_quest(self):
        response = self.client.get('/user/{}/quest/{}/'.format('user2', '1'))
        self.assertEqual(response.status_code, 404)
        # self.assertContains(response, "User doesn't have this quest")

    def test_get_user_info_no_user(self):
        response = self.client.get('/user/{}/quest/{}/'.format('chupachups', '1'))
        self.assertEqual(response.status_code, 404)

    def test_post_puzzle_wrong_answer(self):
        response = self.client.post('/user/{}/quest/{}/'.format('user1', '1'), {'answer': 'Бла'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'wrong')

    def test_post_puzzle_correct_answer(self):
        response = self.client.post('/user/{}/quest/{}/'.format('user1', '1'), {'answer': 'Кремль'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'correct')


class PlaceInfoViewTest(TestCase):
    def test_get_user_info_ok(self):
        response = self.client.get('/user/{}/quest/{}/place/{}/fact/{}/'.format('user1', '1', '1', '1'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'User User')
        self.assertContains(response, 'puzzle')
        self.assertContains(response, 'quest')
        self.assertContains(response, 'places_ids')
        self.assertContains(response, 'place')
        self.assertContains(response, 'fact')

    def test_get_user_info_no_user(self):
        response = self.client.get('/user/{}/quest/{}/place/{}/fact/{}/'.format('chupachups', '1', '1', '1'))
        self.assertEqual(response.status_code, 404)

    def test_get_user_no_such_quest(self):
        response = self.client.get('/user/{}/quest/{}/place/{}/fact/{}/'.format('user1', '0', '1', '1'))
        self.assertEqual(response.status_code, 404)

    def test_get_user_not_his_quest(self):
        response = self.client.get('/user/{}/quest/{}/place/{}/fact/{}/'.format('user2', '1', '1', '1'))
        self.assertEqual(response.status_code, 404)

    def test_get_user_no_such_puzzle(self):
        response = self.client.get('/user/{}/quest/{}/place/{}/fact/{}/'.format('user1', '1', '0', '1'))
        self.assertEqual(response.status_code, 404)

    def test_get_user_no_such_fact(self):
        response = self.client.get('/user/{}/quest/{}/place/{}/fact/{}/'.format('user1', '1', '1', '0'))
        self.assertEqual(response.status_code, 404)

    def test_get_bad_request(self):
        response = self.client.get('/user/{}/quest/{}/place/{}/fact/{}/'.format('user1', '1', '3', '1'))
        self.assertEqual(response.status_code, 400)


class NewQuestViewTest(TestCase):
    def test_post_new_quest_ok(self):
        response = self.client.post('/user/{}/quest/'.format('user1'))
        self.assertEqual(response.status_code, 201)

    def test_post_quest_no_user(self):
        response = self.client.post('/user/{}/quest/'.format('chupachups'))
        self.assertEqual(response.status_code, 404)
