Periodic tasks for h
====================

This contains the necessary configuration for running celery beat to schedule
periodic tasks that the celery workers in `h` will pick up.

While this will be used as a docker container on production/staging, for
development purposes this needs to run manually with `celery -A hperiodic beat`

Docker example
--------------

.. code-block:: bash

   $ make docker
   $ docker run \
       -p 8080:8080
       -e BROKER_URL=amqp://user:password@rabbitmq.host//virtual-host \
       hypothesis/h-periodic:dev
