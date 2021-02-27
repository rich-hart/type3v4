from pymongo import MongoClient
from pymemcache.client.base import Client as CacheClient
import boto3

from django.conf import settings

class Client:
    name = None
    _connection = None
    _cursor = None
    _instance = None
    _db = None
    _collection = None


    def __call__(self):
        """
        Change project client to service client
        with function call e.g. project_client = Client()
        service_client = project_client()
        """
        return self._instance

    @property
    def instance(self):
        if not self._instance:
            raise NotImplementedError()
        return self._instance

    def reload(self):
        self._instance = None
        self.instance


class S3(Client):
    name = 's3'


    def __init__(
            self,
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        ):
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.instance

    @property
    def instance(self):
        if not self._instance:
            self._instance = boto3.client(
                self.name,
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )
        return self._instance


class Cache(Client):
    name = 'cache'
    host = settings.MEMCACHED_HOST
    port = settings.MEMCACHED_PORT

    def __init__(self):
        self._instance = CacheClient((self.host,self.port))


    @property
    def instance(self):
        if not self._instance:
            self._instance = CacheClient((self.host,self.port))
        return self._instance


class Mongo(Client):
    name = 'mongo'
#    MONGO_URI = f'mongodb://' \
#                f'{settings.MONGO_USERNAME}:' \
#                f'{settings.MONGO_PASSWORD}@' \
#                f'{settings.MONGO_HOST}:' \
#                f'{settings.MONGO_PORT}'
    MONGO_URI = settings.MONGO_URL
#    _db = None
#    _collection = None

    def __init__(self):
        self._instance = MongoClient(self.MONGO_URI)
        self._db = self._instance[settings.MONGO_DATABASE]

    @property
    def instance(self):
        if not self._instance:
            self._instance = MongoClient(self.MONGO_URI)
        return self._instance

    @property
    def db(self):
        if not self._db:
            self._db = self.instance[settings.MONGO_DATABASE]
        return self._db
