"""Celery beat scheduler process configuration."""

import sys
from datetime import timedelta
from os import environ

from celery import Celery


def asbool(value):
    """Return True if value is any of "t", "true", "y", etc (case-insensitive)."""
    return str(value).strip().lower() in ("t", "true", "y", "yes", "on", "1")


# We don't want periodic tasks for h-qa because h-qa and h-prod share the same
# database and search index.
# See https://github.com/hypothesis/playbook/issues/436
# So we'll set this DISABLE_H_BEAT envvar on h-qa.
if asbool(environ.get("DISABLE_H_BEAT")):  # pragma: nocover
    print("h_beat disabled by DISABLE_H_BEAT environment variable")
    sys.exit()

celery = Celery("h")
celery.conf.update(
    beat_schedule_filename="h-celerybeat-schedule",
    beat_schedule={
        "purge-deleted-annotations": {
            "options": {"expires": 1800},
            "task": "h.tasks.cleanup.purge_deleted_annotations",
            "schedule": timedelta(hours=1),
        },
        "purge-expired-authtickets": {
            "options": {"expires": 1800},
            "task": "h.tasks.cleanup.purge_expired_auth_tickets",
            "schedule": timedelta(hours=1),
        },
        "purge-expired-authzcodes": {
            "options": {"expires": 1800},
            "task": "h.tasks.cleanup.purge_expired_authz_codes",
            "schedule": timedelta(hours=1),
        },
        "purge-expired-tokens": {
            "options": {"expires": 1800},
            "task": "h.tasks.cleanup.purge_expired_tokens",
            "schedule": timedelta(hours=1),
        },
        "purge-removed-features": {
            "options": {"expires": 5400},
            "task": "h.tasks.cleanup.purge_removed_features",
            "schedule": timedelta(hours=6),
        },
        "sync-annotations": {
            "options": {"expires": 30},
            "task": "h.tasks.indexer.sync_annotations",
            "schedule": timedelta(minutes=1),
            "kwargs": {"limit": 2500},
        },
        "report-sync-annotations-queue-length": {
            "options": {"expires": 30},
            "task": "h.tasks.indexer.report_job_queue_metrics",
            "schedule": timedelta(minutes=1),
        },
    },
    task_serializer="json",
)
