from django.test import TestCase, Client


class InitialTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_work_weather(self):
        response = self.client.post('/', {'place': 'Москва'})
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        content = response.content.decode()
        self.assertIn('Москва', content)

    def test_weather_non_existent(self):
        response = self.client.post('/', {'place': 'ормпвосриывлофсрилгшр'})
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        content = response.content.decode()
        self.assertIn('Город не найден', content)

    def test_history(self):
        self.client.post('/', {'place': 'Москва'})
        self.client.post('/', {'place': 'Санкт-Петербург'})
        self.client.post('/', {'place': 'ормпвосриывлофсрилгшр'})
        response = self.client.get('/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        content = response.content.decode()
        self.assertIn('Москва', content)
        self.assertIn('Санкт-Петербург', content)
        self.assertNotIn('ормпвосриывлофсрилгшр', content)

    def test_count_bd(self):
        self.client.post('/', {'place': 'Москва'})
        self.client.post('/', {'place': 'ормпвосриывлофсрилгшр'})
        response = self.client.get('/count_cities/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        content = response.content.decode()
        self.assertIn('Москва', content)
        self.assertNotIn('ормпвосриывлофсрилгшр', content)

        self.client.post('/', {'place': 'Москва'})
        response = self.client.get('/count_cities/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        content = response.content.decode()
        self.assertIn('2', content)
