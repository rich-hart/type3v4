from django.shortcuts import render
import django_filters
from rest_framework import viewsets

from .serializers import *

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['object_id']

#    def perform_create(self, serializer):
#        pass

