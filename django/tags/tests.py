from django.conf import settings
from django.test import TestCase

from django.contrib.auth.models import User


from users.models import Profile
from .views import *

class TestSpace(TestCase):
    def test_applications(self):
        self.assertEqual(
            ApplicationSpace.objects.count(),
            len(settings.BASE_INSTALLED_APPS)
        )

class TestTag(TestCase):
    def test_project_tag(self):
        user = User.objects.create()
        tag = Project.add_tag(user.profile)
        expected = user.profile
        returned = tag.get_object()
        self.assertEqual(expected, returned)  
