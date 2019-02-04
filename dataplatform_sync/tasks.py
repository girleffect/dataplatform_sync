import subprocess
from celery import task
from django.conf import settings


class ShellExecutionException(Exception):
    def __init__(self, *args, **kwargs):
        super(ShellExecutionException, self).__init__(*args, **kwargs)


@task
def gc_data_sync(**kwargs):
    files = kwargs.get('files', '')
    directory = kwargs.get('directory', '')

    host = getattr(settings, 'ISON_HOST', '')
    user = getattr(settings, 'ISON_USER', '')
    password = getattr(settings, 'ISON_PASSWORD', '')

    script = 'scripts/SFTPImport.sh'
    bucket = getattr(settings, 'S3_BUCKET', '')
    secret_key = getattr(settings, 'S3_SECRET_KEY', '')
    access_key = getattr(settings, 'S3_ACCESS_KEY', '')

    command = "sshpass {script} " \
              "-u '{user}' -p '{password}' -h {host} " \
              "-d '{directory}' -f '{files}' " \
              "-s '{secret_key}' -a '{access_key}' -b '{bucket}'" \
        .format(
            script=script,
            directory=directory, files=files,
            password=password, user=user, host=host,
            access_key=access_key, secret_key=secret_key, bucket=bucket
        )
    res = subprocess.run(command, shell=True, stderr=subprocess.PIPE)

    if res.returncode > 0:
        raise ShellExecutionException(
            'Error executing {}: {}'.format(script, res.stderr))
    return res