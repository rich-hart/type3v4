import uuid
from django.db import models

from .clients import Mongo, Cache, S3


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    _clients = dict((c.name,c) for c in [
        Mongo(),
        Cache(),
        S3(),
    ])
    @property
    def clients(self):
        return self._clients

    tag = models.UUIDField(
        primary_key = False,
        unique = True,
        default = uuid.uuid4,
        editable = False,
    )

    @property
    def seed(self):
        return self.tag.int

    @property
    def module_path(self):
        return self.__module__

    @property
    def app_name(self):
        return self.__module__.split('.')[0]

    @property
    def class_name(self):
        return self.__class__.__name__

    class Meta:
        abstract = True

class Object(Base):  #NOTE: Replace Base with Object?  Allow either / or?
    name = models.CharField(max_length=2**6)

