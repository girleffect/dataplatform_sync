import os
import boto3
import datetime
import subprocess
from celery import task
from django.conf import settings
from django.utils import timezone


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
            (timezone.now() - timezone.timedelta(days=2)
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
        ec2 = boto3.resource(
            'ec2',
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        ec2.instances.filter(InstanceIds=[instance_id]).start()


@task(ignore_result=True)
def stop_matillion_instance(**kwargs):
    instance_id = kwargs.get('instance_id')
    if instance_id:
        ec2 = boto3.resource(
            'ec2',
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        ec2.instances.filter(InstanceIds=[instance_id]).stop()


@task(ignore_result=True)
def run_ge_sm(**kwargs):
    from ge_sm.control import pathname as directory, upload_dir

    bucket = getattr(settings, 'S3_BUCKET', '')
    secret_key = getattr(settings, 'S3_SECRET_KEY', '')
    access_key = getattr(settings, 'S3_ACCESS_KEY', '')

    cmd1 = 's3cmd sync --secret_key=${secret_key} --access_key=${access_key} '\
        '${dir}/ s3://${bucket}${dir}/'.format(
            dir=upload_dir,
            bucket=bucket,
            secret_key=secret_key,
            access_key=access_key
        )

    cmd2 = 'rm ${dir}/*'.format(dir=directory)

    try:
        from ge_sm import control
        today = datetime.datetime.now()
        tm = datetime.datetime.strftime(
            today + datetime.timedelta(days=2), "%Y-%m-%d")
        start = os.environ.get('START_DATE', '2019-06-01'),
        end = os.environ.get('END_DATE', '2019-08-01')
        control.main(start, end, tm)
        subprocess.run(cmd1, shell=True, stderr=subprocess.PIPE)
        subprocess.run(cmd2, shell=True, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        raise ShellExecutionException(
            'Error executing ge_sm.control: {}'.format(e))
