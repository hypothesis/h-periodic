"""Celery beat scheduler process configuration."""

from datetime import timedelta

from celery import Celery

celery = Celery("h")
celery.conf.update(
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
