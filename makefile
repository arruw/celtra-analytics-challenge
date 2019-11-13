up:
	docker volume create celtra_db
	docker-compose up -d --build

scale:
	docker-compose scale spark-worker=$(n)

down:
	docker-compose down

clean:
	docker volume rm celtra_db