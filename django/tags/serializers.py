import os


from rest_framework import serializers

from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(TagSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class AssociationSerializer(TagSerializer):
    class Meta:
        model = Association
        fields = '__all__'



