from django.urls import reverse
from django.test import TestCase
from django.core.files.base import File as FileField, ContentFile

from .views import *
from .tasks import *
class TestFiles(TestCase):
    def setUp(self):
        File.objects.all().delete()

    def test_csv_upload(self):
        url = reverse('file-list')
        with open('data/tests/test.csv') as fp:
            data = {'instance': fp}
            responce = self.client.post(url, data)
        expected = 201
        returned = response.status_code
        self.assertEqual(expected,returned)

    def test_parse_csv(self):
        import ipdb; ipdb.set_trace()
        with open('data/tests/test.csv','rb') as fp:
            file = File.objects.create(_instance=FileField(fp))
        tag_id = parse_csv(str(file.object_id))
            
