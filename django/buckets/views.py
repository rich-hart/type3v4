from celery import chain, signature

from django.shortcuts import render
import django_filters
from rest_framework import viewsets
from rest_framework.decorators import action

from tags.models import Project as Tag

from .serializers import *
from .tasks import *

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['object_id']

    def perform_create(self, serializer):
        file = serializer.save()
        if file.instance.name.endswith('.csv'):
            args = (str(file.object_id),file.has_headers)
            #result = parse_csv.apply_async(args, link=stanford_nlp.s()) 
            result = chain(parse_csv.s(*args), stanford_nlp.s())() 
            task_data = { 
                'nlp_task_id' : str(result.task_id),
                'parse_task_id' : str(result.parent.task_id),
            }
            tag = Tag.add_tag(file, name='tasks', data=task_data)
             
            
