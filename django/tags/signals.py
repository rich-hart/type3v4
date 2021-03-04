import os
from django.conf import settings
from tagging.models import Tag as DjangoTag
from django.apps import apps
from .serializers import *

def load_application_space(sender, **kwargs):
    for app in set(settings.BASE_INSTALLED_APPS):
        ApplicationSpace.objects.get_or_create(name=app)   


def load_namespace(sender, **kwargs):
    namespaces = []
    for file in os.listdir('tags/defs'):
        if file.endswith('.yml') or file.endswith('.yaml'):
            name = file.split('.')[0].upper()
            NameSpace.objects.get_or_create(name=name)   
    NameSpace.objects.get_or_create(name="")


def load_model_space(sender, **kwargs):
    applications = set(settings.BASE_INSTALLED_APPS)
    for app in applications:
        for model in  apps.get_app_config(app).get_models():
            ModelSpace.objects.get_or_create(name=model._meta.object_name)


def save_project_tag(sender, instance, created, **kwargs):
    if created:
        object = instance.get_object()
        mongo = object.clients['mongo']
        collection = mongo.db[object.class_name]
        data = ProjectSerializer(instance).data
        collection.update(spec={'_id': data['_id']},document=data,upsert=True)
        instance._data={}
        instance.save()


def save_accociation_tag(sender, instance, created, **kwargs):
    if created:
        mongo = instance.clients['mongo']
        collection = mongo.db[sender.__class__.__name__]
        data = AssociationSerializer(instance).data
        parent = Tag.objects.get(_id=instance.parent_id)
        object=parent.get_object()
        DjangoTag.objects.add_tag(object,instance._id.hex)
        collection.update(spec={'_id': data['_id']},document=data,upsert=True)
        instance._data={}
        instance.save()


 
