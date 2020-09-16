Periodic tasks for h
====================

`h-periodic` runs a [Celery beat](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)
process for scheduling periodic tasks for h's Celery workers to execute.

## Installing h-periodic in a development environment

### You will need

* h-periodic connects to the RabbitMQ process that h's `make dev` command runs,
  so you'll need to install and run h first:

  * https://h.readthedocs.io/en/latest/developing/install/

* [Git](https://git-scm.com/)

* [pyenv](https://github.com/pyenv/pyenv)
  Follow the instructions in the pyenv README to install it.
  The Homebrew method works best on macOS.

### Clone the Git repo

    git clone https://github.com/hypothesis/h-periodic.git

This will download the code into an `h-periodic` directory in your current
working directory. You need to be in the `h-periodic` directory from the
remainder of the installation process:

    cd h-periodic

### Start the development server

    make dev

The first time you run `make dev` it might take a while to start because it'll
need to install the dependencies.

This will:

1. Start the health check server on <http://localhost:8080/_status>.

   This endpoint is used by Elastic Beanstalk to check h-periodic's health.
   You can also visit it in dev to check if things seem to be working.

2. Start the Celery beat process itself, which periodically adds tasks to h's task queue.

**That's it!** You’ve finished setting up your h-periodic development
environment. Run `make help` to see all the commands that're available for
linting, code formatting, etc.
