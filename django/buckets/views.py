from celery import chain, signature

from django.shortcuts import render
import django_filters
from rest_framework import viewsets
from rest_framework.decorators import action

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
            args = (str(file.object_id),)
            parse_csv.apply_async(args, link=stanford_nlp.s()) 

    @action(detail=True, methods=['get'],serializer_class=ParserSerializer)
    def parse(self, request, pk=None):
        import ipdb; ipdb.set_trace()
        file = self.get_object()
        self.serializer_class(instance=file)
        
