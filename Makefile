.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make dev               Run the entire app (web server and other processes)"
	@echo "make lint              Run the code linter(s) and print any warnings"
	@echo "make format            Correctly format the code"
	@echo "make checkformatting   Crash if the code isn't correctly formatted"
	@echo "make test              Run the unit tests and produce a coverage report"
	@echo "make sure              Make sure that the formatter, linter, tests, etc all pass"
	@echo "make docker            Make the app's Docker image"
	@echo "make clean             Delete development artefacts (cached files, "
	@echo "                       dependencies, etc)"
	@echo "make requirements      Compile all requirements files"

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
	# values (see conf/development.ini for non-production quality examples).
	@docker run \
		--net h_default \
		-e BROKER_URL=amqp://guest:guest@rabbit:5672// \
		-p 8080:8080 \
		hypothesis/h-periodic:$(DOCKER_TAG)

.PHONY: clean
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

.PHONY: sure
sure: checkformatting lint test functests

DOCKER_TAG = dev

.PHONY: python
python:
	@./bin/install-python

.PHONY: requirements
requirements:
	@sh requirements/compile.sh
