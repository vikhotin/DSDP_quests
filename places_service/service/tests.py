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


class FactViewTests(TestCase):
    def setUp(self):
        place_1 = Place.objects.create(name='Placename', long='37', lat='56')
        fact = Fact.objects.create(place=place_1, text='Funny fact haha', added_by='admin', is_moderated='True')
        self.id = fact.id

    def test_get_fact_ok(self):
        response = self.client.get('/fact/{}/'.format(self.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Funny fact haha')
        self.assertContains(response, 'admin')

    def test_get_fact_not_exist(self):
        response = self.client.get('/fact/1000/')
        self.assertEqual(response.status_code, 404)


class FactsViewTests(TestCase):
    def setUp(self):
        place_1 = Place.objects.create(name='Placename', long='37', lat='56')
        Fact.objects.create(place=place_1, text='Funny fact haha', added_by='admin', is_moderated='True')
        Fact.objects.create(place=place_1, text='Did you know that?', added_by='admin', is_moderated='True')
        self.fk = place_1.id

    def test_get_facts_ok(self):
        response = self.client.get('/fact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Funny fact haha')
        self.assertContains(response, 'Did you know that?')

    def test_post_fact(self):
        response = self.client.post('/fact/', {'place': '{}'.format(self.fk), 'text': 'succ',
                                               'added_by': 'troll111', 'is_moderated': '0'})
        self.assertEqual(response.status_code, 201)

    def test_post_fact_invalid(self):
        with self.assertRaises(Exception):
            self.client.post('/fact/', {'place': '1000'})


class PuzzleViewTests(TestCase):
    def setUp(self):
        place = Place.objects.create(name='Placename', long='37', lat='56')
        puzzle = Puzzle.objects.create(place=place, text='Answer to life the universe and everything',
                                       answer='42', added_by='normie', is_moderated='True')
        self.id = puzzle.id

    def test_get_puzzle_ok(self):
        response = self.client.get('/puzzle/{}/'.format(self.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Answer to life the universe and everything')
        self.assertNotContains(response, '42')
        self.assertContains(response, 'normie')

    def test_get_puzzle_not_exist(self):
        response = self.client.get('/puzzle/1000/')
        self.assertEqual(response.status_code, 404)

    def test_post_puzzle_wrong_answer(self):
        response = self.client.post('/puzzle/{}/'.format(self.id), {'answer': '41'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'wrong')

    def test_post_puzzle_correct_answer(self):
        response = self.client.post('/puzzle/{}/'.format(self.id), {'answer': '42'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'correct')


class PuzzlesViewTests(TestCase):
    def setUp(self):
        place = Place.objects.create(name='Placename', long='37', lat='56')
        Puzzle.objects.create(place=place, text='Question 1', added_by='normie', is_moderated='True')
        Puzzle.objects.create(place=place, text='Question 2', added_by='normie', is_moderated='True')
        self.fk = place.id

    def test_get_puzzles_ok(self):
        response = self.client.get('/puzzle/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Question 1')
        self.assertContains(response, 'Question 2')

    def test_post_puzzle(self):
        response = self.client.post('/puzzle/', {'place': '{}'.format(self.fk), 'text': 'succ',
                                                 'answer': 'sipp', 'added_by': 'orang', 'is_moderated': '0'})
        self.assertEqual(response.status_code, 201)

    def test_post_puzzle_invalid(self):
        with self.assertRaises(Exception):
            response = self.client.post('/puzzle/', {'place': '1000', 'text': 'succ',
                                                     'answer': 'sipp', 'added_by': 'orang', 'is_moderated': '0'})
