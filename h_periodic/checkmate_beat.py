"""Celery beat scheduler process configuration."""
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

celery = Celery("checkmate")
celery.conf.update(
    task_queues=[
        Queue(
            "celery",
            # We don't care if the messages are lost if the broker restarts
            durable=False,
            routing_key="celery",
            exchange=Exchange("celery", type="direct", durable=False),
        ),
    ],
    beat_schedule_filename="checkmate-celerybeat-schedule",
    beat_schedule={
        "sync-blocklist": {
            "options": {"expires": 30},
            "task": "checkmate.celery_async.tasks.sync_blocklist",
            "schedule": timedelta(minutes=1),
        },
        # Timings are listed here: https://urlhaus.abuse.ch/api/#retrieve
        # The full list is requested to be fetch less than every 5 minutes, but
        # this is massive overkill as we also use the second update list, which
        # covers the last 30 days
        "initialise-urlhaus": {
            "options": {"expires": 43200},
            "task": "checkmate.celery_async.tasks.initialize_urlhaus",
            # Execute at midnight (once per day)
            "schedule": crontab(hour=0, minute=0),
        },
        "sync-urlhaus": {
            "options": {"expires": 900},
            "task": "checkmate.celery_async.tasks.sync_urlhaus",
            # Execute at quarter past the hour and quarter to (once per 30 min)
            "schedule": crontab(minute="15,45"),
        },
    },
    task_serializer="json",
)
