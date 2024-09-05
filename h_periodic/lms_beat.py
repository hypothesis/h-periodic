"""Celery beat scheduler process configuration."""

import sys
from datetime import timedelta
from os import environ

from celery import Celery
from celery.schedules import crontab

from h_periodic._util import asbool

if asbool(environ.get("DISABLE_LMS_BEAT")):  # pragma: nocover
    print("lms_beat disabled by DISABLE_LMS_BEAT environment variable")
    sys.exit()


# pylint: disable=duplicate-code
celery = Celery("lms")
celery.conf.update(
    beat_schedule_filename="lms-celerybeat-schedule",
    beat_schedule={
        "rotate-rsa-keys": {
            "options": {"expires": 600},
            "task": "lms.tasks.rsa_key.rotate_keys",
            "schedule": timedelta(hours=1),
        },
        "send_instructor_email_digests": {
            "task": "lms.tasks.email_digests.send_instructor_email_digest_tasks",
            "schedule": crontab(hour=7, minute=15),
        },
        "refresh_hubspot_data": {
            "task": "lms.tasks.hubspot.refresh_hubspot_data",
            "schedule": crontab(hour=13, minute=0),
        },
        "export_companies_contract_billables": {
            "task": "lms.tasks.hubspot.export_companies_contract_billables",
            "schedule": crontab(hour=14, minute=0),
        },
        "schedule_monthly_deal_report": {
            "task": "lms.tasks.organization.schedule_monthly_deal_report",
            "schedule": timedelta(minutes=15),
            "kwargs": {"limit": 2, "backfill": 20},
        },
        "schedule_fetching_rosters": {
            "task": "lms.tasks.roster.schedule_fetching_rosters",
            "schedule": timedelta(minutes=15),
        },
        "delete_expired_task_done_rows": {
            "task": "lms.tasks.task_done.delete_expired_rows",
            "options": {"expires": 1800},
            "schedule": timedelta(hours=1),
        },
    },
)
