# Generated by Django 3.1.7 on 2021-03-13 20:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSpace',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('key', models.UUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModelSpace',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('key', models.UUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NameSpace',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('key', models.UUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('_data', models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('tag_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tags.tag')),
                ('api', models.UUIDField(default=uuid.UUID('66533a7d-66bb-3586-8959-592be1b228e1'), editable=False)),
                ('application', models.UUIDField(editable=False)),
                ('model', models.UUIDField(editable=False)),
                ('object', models.UUIDField(editable=False)),
                ('name', models.UUIDField(default=uuid.UUID('7aaf118c-f174-3eba-9ec5-680cd791a020'), editable=False)),
            ],
            options={
                'unique_together': {('api', 'application', 'model', 'object', 'name')},
            },
            bases=('tags.tag',),
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('tag_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tags.tag')),
                ('parent_id', models.UUIDField(editable=False, null=True)),
                ('child_id', models.UUIDField(editable=False, null=True)),
                ('parent_object_id', models.UUIDField(editable=False, null=True)),
                ('child_object_id', models.UUIDField(editable=False, null=True)),
            ],
            options={
                'unique_together': {('parent_id', 'parent_object_id', 'child_id', 'child_object_id')},
            },
            bases=('tags.tag',),
        ),
    ]
