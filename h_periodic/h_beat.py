"""Celery beat scheduler process configuration."""

import sys
from datetime import timedelta
from os import environ

from celery import Celery

from h_periodic._util import asbool

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
            "schedule": timedelta(minutes=5),
        },
        "report-num-deleted-annotations": {
            "options": {"expires": 30},
            "task": "h.tasks.cleanup.report_num_deleted_annotations",
            "schedule": timedelta(minutes=1),
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
        "purge-deleted-users": {
            "options": {"expires": 1800},
            "task": "h.tasks.cleanup.purge_deleted_users",
            "schedule": timedelta(minutes=5),
        },
        "sync-annotations": {
            "options": {"expires": 30},
            "task": "h.tasks.indexer.sync_annotations",
            "schedule": timedelta(minutes=1),
            "kwargs": {"limit": 400},
        },
        "sync-slim-annotations": {
            "options": {"expires": 30},
            "task": "h.tasks.annotations.sync_annotation_slim",
            "schedule": timedelta(minutes=1),
            "kwargs": {"limit": 1000},
        },
        "delete_expired_task_done_rows": {
            "task": "h.tasks.task_done.delete_expired_rows",
            "options": {"expires": 1800},
            "schedule": timedelta(hours=1),
        },
        "report-sync-annotations-queue-length": {
            "options": {"expires": 30},
            "task": "h.tasks.indexer.report_job_queue_metrics",
            "schedule": timedelta(minutes=1),
        },
    },
)
