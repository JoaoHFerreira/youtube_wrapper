clean:
	rm *.txt --yes; rm *.json --yes

build:
	docker compose build scrapy

run:
	docker compose run --rm scrapy python main.py $(command)


debug:
	docker compose run --rm scrapy /bin/bash

scraper-clean:
	rm scrape/articles/*