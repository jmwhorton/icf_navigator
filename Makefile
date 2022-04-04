TAG=$(shell git rev-parse --short HEAD)
IMAGE_NAME=jrutecht/icf_navigator
.PHONY: push clean

default: build

build:
	docker build . -t ${IMAGE_NAME}:${TAG} -t ${IMAGE_NAME}:latest
	date > last_built

push:
	docker image push ${IMAGE_NAME}:${TAG}
	docker image push ${IMAGE_NAME}:latest

clean:
	rm -f last_built

