build:
	docker compose build scrapy

run:
	docker compose run --rm scrapy python main.py

debug:
	docker compose run --rm scrapy /bin/bash


query:
	docker compose run --rm scrapy python interactive.py