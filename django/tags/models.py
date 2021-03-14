import enum
import os
import uuid
from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.apps import apps
from django.utils import timezone

from tagging.models import Tag as DjangoTag

from project.models import Base

DEFAULT_API_ID = uuid.uuid3(uuid.NAMESPACE_X500, settings.API_VERSION)
ROOT_NAMESPACE = uuid.uuid3(uuid.NAMESPACE_X500, '')

class Space(Base):
    name = models.CharField(max_length=2**6)
    key = models.UUIDField(
        primary_key = True,
        editable = False,
    )
    object_id = None

    @staticmethod
    def get_value(name):
        return uuid.uuid3(uuid.NAMESPACE_X500,name)

    def save(self, *args, **kwargs):
        self.key = self.get_value(self.name)
        super(Space, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class NameSpace(Space):
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(NameSpace, self).save(*args, **kwargs)

class ApplicationSpace(Space):
    pass

class ModelSpace(Space):
    pass

def build_uuid(*uids):
    uids = list(uids)
    if not uids:
        return
    new_id = uids.pop(0)
    for uid in uids:
        new_id = uuid.uuid3(new_id, uid.hex)
    return new_id

class Tag(Base):
    _id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = True,
    )
    _data = JSONField(default=dict)
    object_id = None

class Project(Tag):
    api = models.UUIDField(editable=False,null=False, default=DEFAULT_API_ID)
    application = models.UUIDField(editable=False,null=False)
    model = models.UUIDField(editable=False,null=False)
    object =  models.UUIDField(editable=False,null=False)
    name = models.UUIDField(editable=False,null=False, default=ROOT_NAMESPACE)

    @property
    def data(self):
        mongo = self.clients['mongo']
        class_name = ModelSpace.objects.get(key=self.model).name
        collection = mongo.db[class_name]
        data = collection.find_one({"_id" :str(self._id)}) or {}
        data = data.get('_data',{})
        return data

    def build(self):
        attributes = []
        for field in Project._meta.get_fields():
            if isinstance(field, models.UUIDField):
                attributes.append(field)
        attributes = [
            getattr(self,a.name) or '' 
            for a in attributes if '_' not in a.name
        ]
        self._id = build_uuid(*attributes)

    def save(self, *args, **kwargs):
        self.build()
        super(Project, self).save(*args, **kwargs)

    def get_object(self):
        object = None
        if self.application and self.model and self.object: 
            app_label = ApplicationSpace.objects.get(key=self.application).name
            model_name = ModelSpace.objects.get(key=self.model).name
            model = apps.get_model(app_label=app_label, model_name=model_name)
            object = model.objects.get(object_id=self.object)
        return object

    @classmethod
    def get_tag_id(cls, object, tag_name=''):
        model_id = Space.get_value(object.class_name)
        app_id = Space.get_value(object.app_name)
        object_id = object.object_id
        namespace_id = Space.get_value(tag_name.upper())
        instance = cls(
            application=app_id,
            model=model_id,
            object=object_id,
            name=namespace_id,
        )
        instance.build()
        return instance._id

    @classmethod
    def add_tag(cls, object, name='', data=None):
        model_id = Space.get_value(object.class_name) #FIXME: model from ModelNamespace
        app_id = Space.get_value(object.app_name)
        object_id = object.object_id
        name_id = Space.get_value(name.upper())
        instance = cls(
            application=app_id,
            model=model_id,
            object=object_id,
            name=name_id,
            _data=data or {},
            created = timezone.now(),
            updated = timezone.now(),
        )
        instance.save()
        DjangoTag.objects.add_tag(object, str(instance._id))
#        DjangoTag.objects.add_tag(object, str(namespace_id))
        return instance

    class Meta:
        unique_together = (
            ("api","application","model","object","name"),
        )


class Association(Tag):
    parent_id = models.UUIDField(editable=False,null=True)
    child_id = models.UUIDField(editable=False,null=True)
    parent_object_id = models.UUIDField(editable=False,null=True)
    child_object_id = models.UUIDField(editable=False,null=True)

    def save(self, *args, **kwargs):
        attributes = []
        for field in Association._meta.get_fields():
            if isinstance(field, models.UUIDField):
                attributes.append(field)
        attributes = [getattr(self,a.name) or '' for a in attributes if '_' not in a.name]
        self._id = build_uuid(*attributes)
        super(Association, self).save(*args, **kwargs)

    class Meta:
        unique_together =  (
            ("parent_id", "parent_object_id","child_id","child_object_id")
        )

