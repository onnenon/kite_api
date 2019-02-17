dbup:
	docker run --rm -d \
		--name test-db \
		-p 5432:5432 \
		-e "POSTGRES_USER=admin" \
		-e "POSTGRES_PASSWORD=pass" \
		-e "POSTGRES_DB=forum_db" \
		postgres:9.6-alpine

dbdown:
	docker kill test-db

up:
	docker-compose up -d

exec:
	docker-compose exec api bash

down:
	docker-compose down

run:
	flask run --host=0.0.0.0

test: dbup
	pip install -r requirements-test.txt
	bash run-tests.sh
