from django.urls import reverse
from django.test import TestCase
from django.core.files.base import File as FileField, ContentFile

from .views import *
from .tasks import *
class TestFiles(TestCase):
    def setUp(self):
        File.objects.all().delete()

    def test_csv_upload(self):
        import ipdb; ipdb.set_trace()
        url = reverse('file-list')
        with open('data/tests/test.csv') as fp:
            data = {'instance': fp,'has_headers': True}
            response = self.client.post(url, data)
        expected = 201
        returned = response.status_code
        self.assertEqual(expected,returned)

    def test_parse_csv(self):
        with open('data/tests/test.csv','rb') as fp:
            file = File.objects.create(_instance=FileField(fp))
        tag_id = parse_csv(str(file.object_id))
        tag = Tag.objects.get(_id=tag_id) 
        returned = tag.data
        self.assertTrue(returned)
        return str(tag._id)

    def test_nlp_task(self):
        tag_id = self.test_parse_csv()
        new_tag_id = stanford_nlp(tag_id)
        self.assertNotEqual(tag_id,new_tag_id)
        tag = Tag.objects.get(_id=new_tag_id)
        returned = tag.data
        self.assertTrue(returned)
        return str(tag._id)

    def test_parse_view(self):
        import ipdb; ipdb.set_trace()       
        tag_id = self.test_nlp_task()
        tag = Tag.objects.get(_id=tag_id)
        file = tag.get_object()
        url = reverse('file-detail', kwargs={'pk': str(file.object_id)})
        response = self.client.get(url)
