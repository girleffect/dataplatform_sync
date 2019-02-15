FROM index.docker.io/praekeltfoundation/django-bootstrap:latest

COPY . /app
RUN pip install -e .

ENV DJANGO_SETTINGS_MODULE dataplatform_sync.settings
ENV CELERY_APP proj

RUN apt-get update && apt-get install -y  sshpass

CMD ["dataplatform_sync.wsgi:application"]