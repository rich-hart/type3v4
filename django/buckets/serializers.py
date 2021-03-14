from celery.result import AsyncResult
from project.celery import app as celery_app 

from rest_framework import serializers
from tagging.models import Tag as DjangoTag, TaggedItem as DjangoTaggedItem

from tags.models import Project as Tag

from .models import *

class FileSerializer(serializers.ModelSerializer):
    instance = serializers.FileField()
    headers = serializers.ListField(read_only=True)
    rows = serializers.JSONField(read_only=True)
    temporals = serializers.JSONField(read_only=True)
    parse_status = serializers.CharField(read_only=True)
    nlp_status = serializers.CharField(read_only=True)
    has_headers = serializers.BooleanField(write_only=True)
    class Meta:
        model = File
        fields = (
            'object_id',
            'instance',
            'headers',
            'rows',
            'temporals',
            'has_headers',
            'parse_status',
            'nlp_status',
        )

    def to_representation(self, instance):
        import ipdb; ipdb.set_trace()
        instance.headers = []
        instance.rows = {}
        instance.temporals = {}
        instance.parse_status = ''
        instance.nlp_status = ''

        tag_id = Tag.get_tag_id(instance, 'tasks')
        tasks_tag = Tag.objects.filter(_id = tag_id).first() or {}

        if tasks_tag:

            nlp_task_id = tasks_tag.data.get('nlp_task_id','')
            nlp_result = AsyncResult(nlp_task_id,app=celery_app)
            instance.nlp_status = nlp_result.status

            parse_task_id = tasks_tag.data.get('parse_task_id','')
            parse_result = AsyncResult(parse_task_id,app=celery_app)
            instance.parse_status = parse_result.status

        rep = super(FileSerializer, self).to_representation(instance)
        return rep

    def create(self, validated_data):
        validated_data['_instance'] = validated_data.pop('instance')
        has_headers = validated_data.pop('has_headers')
        instance = File.objects.create(**validated_data)
        instance.has_headers = has_headers
        return instance

class ParserSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('headers', 'rows', 'temporals')

    def to_representation(self, instance):
        import ipdb; ipdb.set_trace()
        rep = super(FileSerializer, self).to_representation(instance)
        return rep
