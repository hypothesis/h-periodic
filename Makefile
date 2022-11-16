.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make dev               Run the entire app (web server and other processes)"
	@echo "make shell             Launch a Python shell in the dev environment"
	@echo "make lint              Run the code linter(s) and print any warnings"
	@echo "make format            Correctly format the code"
	@echo "make checkformatting   Crash if the code isn't correctly formatted"
	@echo "make test              Run the unit tests"
	@echo "make coverage          Print the unit test coverage report"
	@echo "make sure              Make sure that the formatter, linter, tests, etc all pass"
	@echo "make docker            Make the app's Docker image"

.PHONY: services
services:
	@true

.PHONY: db
db:
	@true

.PHONY: dev
dev: python
	@tox -qe dev

.PHONY: devdata
devdata:
	@true

.PHONY: shell
shell: python
	@tox -qe dev --run-command ipython

.PHONY: format
format: python
	@tox -qe format

.PHONY: checkformatting
checkformatting: python
	@tox -qe checkformatting

.PHONY: lint
lint: python
	@tox -qe lint

.PHONY: test
test:
	@tox -q

.PHONY: coverage
coverage: python
	@tox -qe coverage

.PHONY: functests
functests:
	@true

.PHONY: docker
docker:
	@git archive --format=tar.gz HEAD | docker build -t hypothesis/h-periodic:$(DOCKER_TAG) -

.PHONY: run-docker
run-docker:
	# To run the Docker container locally, first build the Docker image using
	# `make docker` and then set the environment variables below to appropriate
	# values.
	@docker run \
		--net h_default \
		-e BROKER_URL=amqp://guest:guest@rabbit:5672// \
		-p 8080:8080 \
		hypothesis/h-periodic:$(DOCKER_TAG)

# Tell make how to compile requirements/*.txt files.
#
# `touch` is used to pre-create an empty requirements/%.txt file if none
# exists, otherwise tox crashes.
#
# $(subst) is used because in the special case of making requirements.txt we
# actually need to touch dev.txt not requirements.txt and we need to run
# `tox -e dev ...` not `tox -e requirements ...`
#
# $(basename $(notdir $@))) gets just the environment name from the
# requirements/%.txt filename, for example requirements/foo.txt -> foo.
requirements/%.txt: requirements/%.in
	@touch -a $(subst requirements.txt,dev.txt,$@)
	@tox -qe $(subst requirements,dev,$(basename $(notdir $@))) --run-command 'pip --quiet --disable-pip-version-check install pip-tools'
	@tox -qe $(subst requirements,dev,$(basename $(notdir $@))) --run-command 'pip-compile --allow-unsafe --quiet $(args) $<'

# Inform make of the dependencies between our requirements files so that it
# knows what order to re-compile them in and knows to re-compile a file if a
# file that it depends on has been changed.
requirements/dev.txt: requirements/requirements.txt
requirements/tests.txt: requirements/requirements.txt
requirements/functests.txt: requirements/requirements.txt
requirements/lint.txt: requirements/tests.txt requirements/functests.txt

# Add a requirements target so you can just run `make requirements` to
# re-compile *all* the requirements files at once.
#
# This needs to be able to re-create requirements/*.txt files that don't exist
# yet or that have been deleted so it can't just depend on all the
# requirements/*.txt files that exist on disk $(wildcard requirements/*.txt).
#
# Instead we generate the list of requirements/*.txt files by getting all the
# requirements/*.in files from disk ($(wildcard requirements/*.in)) and replace
# the .in's with .txt's.
.PHONY: requirements requirements/
requirements requirements/: $(foreach file,$(wildcard requirements/*.in),$(basename $(file)).txt)

.PHONY: sure
sure: checkformatting lint test coverage functests

DOCKER_TAG = dev

.PHONY: python
python:
	@./bin/install-python
