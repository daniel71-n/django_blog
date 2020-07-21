from django.test import TestCase
from django.test import SimpleTestCase
# Create your tests here.

class SimpleTests(SimpleTestCase):
    def test_home_page_status_code(self):  #see if making an http request for the bare url returns an http 200 (successfull) code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_page_status_code(self):     #see if making an http request for the /about url returns an http 200 (successfull) code
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
