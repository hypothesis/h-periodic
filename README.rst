Periodic tasks for h
====================

This contains the necessary configuration for running celery beat to schedule
periodic tasks that the celery workers in `h` will pick up.

While this will be used as a docker container on production/staging, for
development purposes this needs to run manually with `celery -A hperiodic beat`
