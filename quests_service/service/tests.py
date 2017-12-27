from django.test import TestCase
from .models import Place, Fact, Puzzle


class PlaceViewTests(TestCase):
    def setUp(self):
        place = Place.objects.create(name='Placename', long='37', lat='56')
        self.id = place.id

    def test_get_place_ok(self):
        response = self.client.get('/place/{}/'.format(self.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Placename')
        self.assertContains(response, '37')
        self.assertContains(response, '56')

    def test_get_place_not_exist(self):
        response = self.client.get('/place/1000/')
        self.assertEqual(response.status_code, 404)


class PlacesViewTests(TestCase):
    def setUp(self):
        Place.objects.create(name='Placename', long='37', lat='56')
        Place.objects.create(name='Anothername', long='57', lat='36')

    def test_get_places_ok(self):
        response = self.client.get('/place/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Placename')
        self.assertContains(response, '37')
        self.assertContains(response, '56')
        self.assertContains(response, 'Anothername')
        self.assertContains(response, '57')
        self.assertContains(response, '36')

    def test_post_place(self):
        response = self.client.post('/place/', {'name': 'Place_ka', 'long': '11', 'lat': '11'})
        self.assertEqual(response.status_code, 201)

    def test_post_place_invalid(self):
        response = self.client.post('/place/', {'name': 'Placename'})
        self.assertEqual(response.status_code, 409)
