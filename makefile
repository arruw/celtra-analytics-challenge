setup:
	env

up:
	docker-compose up -d

down:
	docker-compose down

batch:
	echo "TODO"

gen:
	docker build -t impression-gen services/impression-gen
	docker run --network celtra_default --env-file .env impression-gen
