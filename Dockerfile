FROM praekeltfoundation/django-bootstrap:py3.6

COPY . /app
RUN apt update
RUN apt install -y git-core
RUN pip install -e .

ENV DJANGO_SETTINGS_MODULE dataplatform_sync.settings

RUN apt-get update && apt-get install -y  sshpass s3cmd

CMD ["dataplatform_sync.wsgi:application",  "--timeout", "1800"]
