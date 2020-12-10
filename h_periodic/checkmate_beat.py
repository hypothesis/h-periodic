"""Celery beat scheduler process configuration."""
from datetime import timedelta

from celery import Celery
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
            "task": "checkmate.async.tasks.sync_blocklist",
            "schedule": timedelta(minutes=1),
        },
    },
    task_serializer="json",
)
