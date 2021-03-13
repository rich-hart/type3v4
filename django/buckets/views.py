from django.shortcuts import render
from rest_framework import viewsets

from .serializers import *

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_fields = ['object_id']

#    def perform_create(self, serializer):
#        pass

