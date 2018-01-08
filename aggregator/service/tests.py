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
