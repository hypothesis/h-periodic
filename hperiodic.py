# -*- coding: utf-8 -*-

"""
Celery configuration for a separate beat process.
"""

from __future__ import absolute_import

from datetime import timedelta
import os

from celery import Celery

# This can be imported on any system but properties and methods can only be
# accessed when running on an actual EC2 instance.
from ec2_metadata import ec2_metadata

# Configure the broker transport. These settings need to match the
# configuration of the Celery worker in 'h' which will actually execute the
# tasks.
broker_url = os.getenv('BROKER_URL','')
broker_transport_options = {}
if broker_url.startswith('sqs://'):
    # Prefix for SQS queue names to make it clearer which service the queues
    # are associated with.
    #
    # This is configurable to support different h instances in the same AWS
    # account.
    #
    # This prefix must match the one used for the corresponding h instance.
    queue_name_prefix = os.getenv('SQS_QUEUE_NAME_PREFIX', 'hypothesis-h-')

    broker_transport_options = {
        'queue_name_prefix': queue_name_prefix,

        # Use SQS from the same region as the EC2 instance on which h-periodic
        # is running.
        'region': ec2_metadata.region,
    }

celery = Celery('h')
celery.conf.update(
    broker_transport_options=broker_transport_options,
    beat_schedule={
        'purge-deleted-annotations': {
            'task': 'h.tasks.cleanup.purge_deleted_annotations',
            'schedule': timedelta(hours=1)
        },
        'purge-expired-authtickets': {
            'task': 'h.tasks.cleanup.purge_expired_auth_tickets',
            'schedule': timedelta(hours=1)
        },
        'purge-expired-authzcodes': {
            'task': 'h.tasks.cleanup.purge_expired_authz_codes',
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
    task_serializer='json',
)
