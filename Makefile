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

.PHONY: sure
sure: checkformatting lint test coverage functests

DOCKER_TAG = dev

.PHONY: python
python:
	@./bin/install-python
