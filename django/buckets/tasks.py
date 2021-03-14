import time
import io
import csv
import requests
from celery import shared_task

from buckets.models import *
from tags.models import Project as Tag

STANFORD_URL = 'https://stanford-public.alkymi.cloud/getTemporals'


@shared_task()
def parse_csv(object_id, headers=True):
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
    return str(tag._id)


@shared_task()
def stanford_nlp(tag_id):
    tag = Tag.objects.get(_id=tag_id)
    file = tag.get_object()
    data = []
    for row_id in range(len(tag.data)):
        row = tag.data[row_id]
        for col_id in row:
            cell = tag.data[row_id][col_id]
            url = STANFORD_URL + '?text=' + str(cell)
            response = requests.get(url).json()
            time.sleep(.25) # don't over query server
            if response and isinstance(response,list):
                response = response[0]
                response['row'] = row_id
                response['col'] = col_id
                data.append(response)
    tag = Tag.add_tag(object=file,name='nlp', data=data)
    return str(tag._id)


