import re
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
    from ge_sm.control import path_dir as directory, upload_dir
    fmt = "%Y-%m-%d"
    today = datetime.datetime.now()

    bucket = getattr(settings, 'S3_BUCKET', '')
    secret_key = getattr(settings, 'S3_SECRET_KEY', '')
    access_key = getattr(settings, 'S3_ACCESS_KEY', '')
    kw = dict(
        dir=re.sub(r'^/', '', upload_dir),
        path=directory,
        bucket=bucket,
        secret_key=secret_key,
        access_key=access_key,
        date=datetime.datetime.strftime(today, fmt))

    cmd = 's3cmd mv --secret_key={secret_key} --access_key={access_key} ' \
          's3://{bucket}{dir}/*.csv s3://{bucket}{dir}/archive/{date}/'.format(**kw)

    del kw['date']

    cmd1 = 's3cmd sync --secret_key={secret_key} --access_key={access_key} '\
        '{path}/{dir}/ s3://{bucket}{dir}/'.format(**kw)

    cmd2 = 'rm -rf {path}/{dir}/*'.format(path=directory, dir=upload_dir)

    try:
        from ge_sm import control

        month0 = datetime.datetime.strftime(today.replace(day=1), fmt)
        # 90 days ago
        month1 = datetime.datetime.strftime(
            today - datetime.timedelta(days=90), fmt)

        tm = datetime.datetime.strftime(
            today + datetime.timedelta(days=2), fmt)
        start = os.environ.get('START_DATE', month0)
        end = os.environ.get('END_DATE', month1)

        control.main(start, end, tm)
        for i in [cmd, cmd1, cmd2]:
            res = subprocess.run(i, shell=True, stderr=subprocess.PIPE)
            if not res.returncode == 0:
                raise ShellExecutionException(
                    'Error executing ge_sm.control: {}'.format(res.stderr))

        return True
    except Exception as e:
        raise ShellExecutionException(
            'Error executing ge_sm.control: {}'.format(e))
