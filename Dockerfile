FROM praekeltfoundation/django-bootstrap:py3.6

COPY . /app
RUN pip install -e .

ENV DJANGO_SETTINGS_MODULE dataplatform_sync.settings

RUN apt-get update && apt-get install -y  sshpass

CMD ["dataplatform_sync.wsgi:application"]