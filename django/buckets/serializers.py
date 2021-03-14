from rest_framework import serializers

from .models import *

class FileSerializer(serializers.ModelSerializer):
    instance = serializers.FileField()

    class Meta:
        model = File
        fields = ('object_id', 'instance')

    def create(self, validated_data):
        validated_data['_instance'] = validated_data.pop('instance')
        instance = File.objects.create(**validated_data)
        return instance

class ParserSerializer(serializers.ModelSerializer):
    headers = serializers.ListField()
    rows = serializers.JSONField()
    temporals = serializers.JSONField()

    class Meta:
        model = File
        fields = ('headers', 'rows', 'temporals')

    def to_representation(self, instance):
        import ipdb; ipdb.set_trace()
        rep = super(FileSerializer, self).to_representation(instance)
        return rep
