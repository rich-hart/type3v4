from django.test import TestCase

from .views import *

class TestSignals(TestCase):
    def setUp(self):
        File.objects.all().delete()

    def test_csv_upload(self):
        pass
        with open('data/tests/test.csv') as fp:
            c.post('/customers/wishes/', {'name': 'fred', 'attachment': fp})
