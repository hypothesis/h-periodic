"""Celery beat scheduler process configuration."""
from datetime import timedelta

from celery import Celery

celery = Celery("checkmate")
celery.conf.update(
    beat_schedule_filename="checkmate-celerybeat-schedule",
    beat_schedule={
        "sync-blocklist": {
            "options": {"expires": 30},
            "task": "checkmate.async.tasks.sync_blocklist",
            "schedule": timedelta(minutes=1),
        },
    },
    task_serializer="json",
)
