"""Celery beat scheduler process configuration."""
import sys
from datetime import timedelta
from os import environ

from celery import Celery
from kombu import Exchange, Queue

from h_periodic._util import asbool

if asbool(environ.get("DISABLE_LMS_BEAT")):  # pragma: nocover
    print("lms_beat disabled by DISABLE_LMS_BEAT environment variable")
    sys.exit()


# pylint: disable=duplicate-code
celery = Celery("lms")
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
    beat_schedule_filename="lms-celerybeat-schedule",
    beat_schedule={
        "rotate-rsa-keys": {
            "options": {"expires": 600},
            "task": "lms.tasks.rsa_key.rotate_keys",
            "schedule": timedelta(hours=1),
        },
    },
    task_serializer="json",
)
