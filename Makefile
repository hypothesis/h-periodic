DOCKER_TAG = dev

.PHONY: docker
docker:
	docker build -t hypothesis/h-periodic:$(DOCKER_TAG) .
