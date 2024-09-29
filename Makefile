IMAGE_NAME = minhquan1906/openaichatbot
IMAGE_TAG = latest

.PHONY: all build push up down logs

# App
build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

push: build
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

up:
	docker compose -f docker-compose.yaml up -d

down:
	docker compose -f docker-compose.yaml down

logs:
	docker-compose logs -f

all: build push up
