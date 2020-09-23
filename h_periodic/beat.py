"""Celery beat scheduler process configuration."""

from datetime import timedelta

from celery import Celery

celery = Celery("h")
celery.conf.update(
    beat_schedule={
        "purge-deleted-annotations": {
            "task": "h.tasks.cleanup.purge_deleted_annotations",
            "schedule": timedelta(hours=1),
        },
        "purge-expired-authtickets": {
            "task": "h.tasks.cleanup.purge_expired_auth_tickets",
            "schedule": timedelta(hours=1),
        },
        "purge-expired-authzcodes": {
            "task": "h.tasks.cleanup.purge_expired_authz_codes",
            "schedule": timedelta(hours=1),
        },
        "purge-expired-tokens": {
            "task": "h.tasks.cleanup.purge_expired_tokens",
            "schedule": timedelta(hours=1),
        },
        "purge-removed-features": {
            "task": "h.tasks.cleanup.purge_removed_features",
            "schedule": timedelta(hours=6),
        },
        "backfill-annotation-sequence-ids": {
            "task": "h.tasks.temp.backfill_annotation_sequence_ids",
            "schedule": timedelta(minutes=1),
        },
    },
    task_serializer="json",
)
