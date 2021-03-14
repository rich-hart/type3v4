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

Upload files at [http://localhost/api/files/](http://localhost/api/files/).

Sample file at `django/data/tests/test.csv`.

File list at [http://localhost/api/files/](http://localhost/api/files/).

File detail at http://localhost/api/files/\<id\>/.

Filter files with http://localhost/api/files/?object\_id=\<object\_id\>

