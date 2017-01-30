# -*- coding: utf-8 -*-

"""
Celery configuration for a separate beat process.
"""

from __future__ import absolute_import

from datetime import timedelta

from celery import Celery

celery = Celery('h')
celery.conf.update(
    CELERYBEAT_SCHEDULE={
        'purge-deleted-annotations': {
            'task': 'h.tasks.cleanup.purge_deleted_annotations',
            'schedule': timedelta(hours=1)
        },
        'purge-expired-authtickets': {
            'task': 'h.tasks.cleanup.purge_expired_auth_tickets',
            'schedule': timedelta(hours=1)
        },
        'purge-expired-tokens': {
            'task': 'h.tasks.cleanup.purge_expired_tokens',
            'schedule': timedelta(hours=1)
        },
        'purge-removed-features': {
            'task': 'h.tasks.cleanup.purge_removed_features',
            'schedule': timedelta(hours=6)
        },
    },
    CELERY_TASK_SERIALIZER='json',
)
