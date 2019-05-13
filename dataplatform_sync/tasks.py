import subprocess
from celery import task
from django.conf import settings
from django.utils import timezone
import boto3


class ShellExecutionException(Exception):
    def __init__(self, *args, **kwargs):
        super(ShellExecutionException, self).__init__(*args, **kwargs)


@task(ignore_result=True)
def gc_data_sync(**kwargs):
    files = kwargs.get('files', '')
    directory = kwargs.get('directory', '')
    timestamped_files = kwargs.get('timestamped_files')
    timestamped_format = kwargs.get('timestamped_format')

    if timestamped_files and timestamped_format:
        files = files.format(
            (timezone.now() - timezone.timedelta(days=1)
             ).strftime(timestamped_format)
        )

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


@task(ignore_result=True)
def start_matillion_instance(**kwargs):
    instance_id = kwargs.get('instance_id')
    if instance_id:
        ec2 = boto3.resource('ec2')
        ec2.instances.filter(InstanceIds=instance_id).start()


@task(ignore_result=True)
def stop_matillion_instance(**kwargs):
    instance_id = kwargs.get('instance_id')
    if instance_id:
        ec2 = boto3.resource('ec2')
        ec2.instances.filter(InstanceIds=instance_id).stop()
