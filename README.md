<a href="https://github.com/hypothesis/h-periodic/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/actions/workflow/status/hypothesis/h-periodic/ci.yml?branch=main"></a>
<a><img src="https://img.shields.io/badge/python-3.12-success"></a>
<a href="https://github.com/hypothesis/h-periodic/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pyapp"><img src="https://img.shields.io/badge/cookiecutter-pyapp-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# h-periodic

Celery beat processes for Hypothesis apps.

## Setting up Your h-periodic Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed, run `make --version` to check.
* [pyenv](https://github.com/pyenv/pyenv).
  Follow the instructions in pyenv's README to install it.
  The **Homebrew** method works best on macOS.
  The **Basic GitHub Checkout** method works best on Ubuntu.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).

Then to set up your development environment:

```terminal
git clone https://github.com/hypothesis/h-periodic.git
cd h-periodic
make help
```

## Changing the Project's Python Version

To change what version of Python the project uses:

1. Change the Python version in the
   [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

   ```json
   "python_version": "3.10.4",
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Re-compile the `requirements/*.txt` files.
   This is necessary because the same `requirements/*.in` file can compile to
   different `requirements/*.txt` files in different versions of Python:

   ```terminal
   make requirements
   ```

4. Commit everything to git and send a pull request

## Changing the Project's Python Dependencies

### To Add a New Dependency

Add the package to the appropriate [`requirements/*.in`](requirements/)
file(s) and then run:

```terminal
make requirements
```

### To Remove a Dependency

Remove the package from the appropriate [`requirements/*.in`](requirements)
file(s) and then run:

```terminal
make requirements
```

### To Upgrade or Downgrade a Dependency

We rely on [Dependabot](https://github.com/dependabot) to keep all our
dependencies up to date by sending automated pull requests to all our repos.
But if you need to upgrade or downgrade a package manually you can do that
locally.

To upgrade a package to the latest version in all `requirements/*.txt` files:

```terminal
make requirements --always-make args='--upgrade-package <FOO>'
```

To upgrade or downgrade a package to a specific version:

```terminal
make requirements --always-make args='--upgrade-package <FOO>==<X.Y.Z>'
```

To upgrade **all** packages to their latest versions:

```terminal
make requirements --always-make args=--upgrade
```

## Configuration

| Environment variable     | Usage                                           | Example                                                                                                             |
|--------------------------|-------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `H_BROKER_URL`           | The `h` AMPQ broker                             | `amqp://user:password@rabbit.example.com:5672//`                                                                    |
| `CHECKMATE_BROKER_URL`   | The `checkmate` AMPQ broker                     | `amqp://user:password@rabbit.example.com:5673//`                                                                    |
| `LMS_BROKER_URL`         | The `LMS` AMPQ broker                           | `amqp://user:password@rabbit.example.com:5674//`                                                                    |
| `DISABLE_H_BEAT`         | Whether to disable the `h_beat` process         | `true` to disable the `h_beat` process, `false` to leave it enabled. Defaults to `false` (leave it enabled)         |
| `DISABLE_CHECKMATE_BEAT` | Whether to disable the `checkmate_beat` process | `true` to disable the `checkmate_beat` process, `false` to leave it enabled. Defaults to `false` (leave it enabled) |
| `DISABLE_LMS_BEAT`       | Whether to disable the `lms_beat` process       | `true` to disable, `false` to leave it enabled. Defaults to `false` (leave it enabled)                              |
