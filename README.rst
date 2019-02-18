dataplatform_sync
=================

Celery Task for pulling data from external services

Settings:
=========

> The following settings are required and may be set as ENV Vars or in the the setting files.

`ISON_HOST = None`

`ISON_USER = None`

`ISON_PASSWORD = None`

`S3_BUCKET = None`

`S3_SECRET_KEY = None`

`S3_ACCESS_KEY = None`


Adding Scheduled Tasks
======================

```
    CELERY_BEAT_SCHEDULE = {
        # Executes every Week at 5:30 a.m.
        '<name of schedule>': {
            'task': '<path to task callable eg. tasks.gc_data_sync>',
            'schedule': crontab(hour=5, minute=30, day_of_week=1),
            'args': [<Args for task>],
        },
    }
```
