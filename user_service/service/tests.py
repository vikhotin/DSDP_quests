from django.test import TestCase
from .models import User


class UserViewTests(TestCase):
    def setUp(self):
        User.objects.create(login='user1', password='12345', name='Username')

    def test_get_user_ok(self):
        response = self.client.get('/user/user1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'Username')
        self.assertNotContains(response, '12345')

    def test_get_user_not_exist(self):
        response = self.client.get('/user/chupakabra/')
        self.assertEqual(response.status_code, 404)


class NewUserViewTests(TestCase):
    def setUp(self):
        User.objects.create(login='user1', password='12345', name='Username')

    def test_post_user_ok(self):
        response = self.client.post('/user/', {'login': 'user2', 'password': 'pass2', 'name': 'User_ka'})
        self.assertEqual(response.status_code, 201)

    def test_post_user_already_exists(self):
        response = self.client.post('/user/', {'login': 'user1', 'password': '12345', 'name': 'Username'})
        self.assertEqual(response.status_code, 409)
