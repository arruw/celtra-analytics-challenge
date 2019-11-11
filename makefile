up:
	docker-compose up -d

scale:
	docker-compose scale spark-worker=$(n)

down:
	docker-compose down

agg:
	docker build -t impression-agg services/impression-agg
	docker run --network celtra_default --env-file .env impression-agg

gen:
	docker build -t impression-gen services/impression-gen
	docker run --network celtra_default --env-file .env impression-gen $(days)