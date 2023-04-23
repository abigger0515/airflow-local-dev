.PHONY: build
build:
	docker build . -f Dockerfile --tag airflow:kwliao

.PHONY: version
version:
	docker run --rm --name testairflow airflow:kwliao version

.PHONY: up
up:
	docker compose up -d

.PHONY: down
down: 
	docker compose down
