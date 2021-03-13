import io
import csv
from celery import shared_task

from buckets.models import *
from tags.models import Project as Tag

@shared_task()
def parse_csv(object_id, headers=True):
    import ipdb; ipdb.set_trace()
    file = File.objects.get(object_id=object_id)
    file_binary = file.instance.read()
    data = file_binary.decode('utf-8')
    output = io.StringIO()
    output.write(data)
    output.seek(0)
    reader = csv.reader(output)
    data = []
    for row in reader:
        data.append(row)
    if headers:
        headers = data.pop(0)
    else:
        headers = [str(i) for i in range(len(data[0])) ]
    json_data =  []
    for row in data:
        json_data.append(dict(list(zip(headers,row))))
    tag = Tag.add_tag(object=file,name='csv', data=json_data)
    return tag._id


@shared_task()
def stanford_nlp(*args,**kwargs):
    return args

