from django.test import TestCase
from .models import User


class UserViewTests(TestCase):
    def setUp(self):
        User.objects.create(login='user1', password='12345', name='Username',
                            quests_number='1', quests_completed='0')

    def test_get_user_ok(self):
        response = self.client.get('/user/user1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'Username')
        self.assertNotContains(response, '12345')

    def test_get_user_not_exist(self):
        response = self.client.get('/user/chupakabra/')
        self.assertEqual(response.status_code, 404)

    def test_put_change_user_quests_number(self):
        response = self.client.put('/user/user1/', {'inc': 'quests_number'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"quests_number": "2"')

    def test_put_change_user_quests_completed(self):
        response = self.client.put('/user/user1/', {'inc': 'quests_completed'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"quests_completed": "1"')

    def test_put_change_user_fail(self):
        response = self.client.put('/user/user1/', {'inc': 'smth'})
        self.assertEqual(response.status_code, 400)


class NewUserViewTests(TestCase):
    def setUp(self):
        User.objects.create(login='user1', password='12345', name='Username',
                            quests_number='1', quests_completed='0')

    def test_post_user_ok(self):
        response = self.client.post('/user/', {'login': 'user2', 'password': 'pass2', 'name': 'User_ka'})
        self.assertEqual(response.status_code, 201)

    def test_post_user_already_exists(self):
        response = self.client.post('/user/', {'login': 'user1', 'password': '12345', 'name': 'Username'})
        self.assertEqual(response.status_code, 400)
