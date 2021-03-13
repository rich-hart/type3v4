from rest_framework import serializers

from .models import *

class FileSerializer(serializers.ModelSerializer):
    instance = serializers.FileField()

    class Meta:
        model = File
        fields = ('id', 'object_id', 'instance')

    def create(self, validated_data):
        validated_data['_instance'] = validated_data.pop('instance')
        instance = File.objects.create(**validated_data)
        return instance
