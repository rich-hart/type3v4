from django.db import models
from project.models import Object
from project.storage_backends import MediaStorage

class FSObject(Object):
    owner = models.ForeignKey(
        'users.Profile',
        on_delete=models.CASCADE,
        null=True,
    )
    parent = models.ForeignKey(
        'buckets.FSObject',
        on_delete=models.CASCADE,
        null=True,
        related_name='+'
    )

    @property
    def key(self):
        return self.name
    
    @staticmethod
    def _root(object):
        parent = getattr(object,'parent',None)
        if parent:
            return object._root(parent)
        else:
            return object

    @property
    def root(self):
        return self._root(self)


class Folder(FSObject):
     pass


class File(FSObject):
    _raw = None
    _instance = models.FileField(upload_to='files/%Y/%m/%d')

    def get_bucket(self):
        current_obj = self
        bucket = None
        while current_obj:
            if hasattr(current_obj, 'bucket'):
                bucket = current_obj
                return bucket
            current_obj = current_obj.parent

    @property
    def raw(self):
        return self._raw

    @property
    def instance(self):
        return self._instance


class Text(File): #TEXT
    _text = models.TextField()


class Bucket(FSObject):
    pass



