# socialmedia

## project setup

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd socialmedia
```

2- SetUp venv
```
virtualenv -p python3.10 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements_dev.txt
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py makemigrations
python manage.py migrate
```

6- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

7- run the project
```
python manage.py runserver
```

8- Celery and celery beat
```bash
  celery -A config worker -l info --without-gossip --without-mingle --without-heartbeat
  celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

9- Run tests
```
pytest
```