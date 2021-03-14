# Jobs Pipeline

## Install

```
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec backend python3 manage.py migrate
docker-compose -f docker-compose.prod.yml exec backend python3 manage.py collectstatic
```

Notes:
* collectstatic may error if static files are already built.
* if proxy is not up restart it `docker-compose -f docker-compose.prod.yml up -d proxy`

## Usage

Go to home page at [http://localhost](http://localhost).

View and upload files at [http://localhost/api/files/](http://localhost/api/files/).

Sample file at `django/data/tests/test.csv`.

File detail at `http://localhost/api/files/<id>/`.

Filter files with `http://localhost/api/files/?object_id=<object_id>`

## Support Services

Mongo Express: [http://localhost/mongo](http://localhost/mongo).

RabbitMQ Management [http://localhost/queue](http://localhost/queue).

Adminer [http://localhost/adminer](http://localhost/adminer).

