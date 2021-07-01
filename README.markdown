Periodic tasks
==============

`h-periodic` runs [Celery beat](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)
processes that schedule periodic tasks for `h` and `checkmate`'s Celery workers
to execute.

## Installing h-periodic in a development environment

### You will need

* h-periodic connects to the RabbitMQ processes that `h` and `checkmate`'s
`make services` commands run, so you'll need to install and run them first:

  * https://h.readthedocs.io/en/latest/developing/install/
  * https://github.com/hypothesis/checkmate

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

This will start the Celery beat processes, which periodically add tasks
to `h`'s and `checkmate`'s task queues.

**That's it!** You’ve finished setting up your h-periodic development
environment. Run `make help` to see all the commands that're available for
linting, code formatting, etc.

### Configuration

| Environment variable | Usage | Example |
|----------------------|-------|---------|
| `H_BROKER_URL`         | The `h` AMPQ broker | `amqp://user:password@rabbit.example.com:5672//` |
| `CHECKMATE_BROKER_URL` | The `checkmate` AMPQ broker | `amqp://user:password@rabbit.example.com:5673//` |
| `DISABLE_H_BEAT` | Whether to disable the `h_beat` process | `true` to disable the `h_beat` process, `false` to leave it enabled. Defaults to `false` (leave it enabled) |

