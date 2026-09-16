build:
	docker compose build

build-nc:
	docker compose build --no-cache

down:
	docker compose down --volumes --remove-orphans

run:
	make down && docker compose up

run-scaled:
	make down && docker compose up --scale spark-worker=3

run-d:
	make down && docker compose up -d --scale spark-worker=3

stop:
	docker compose stop

submit:
	docker exec da-spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./apps/$(app)

urls:
	@echo "JupyterLab:      http://localhost:8888/lab?token=spark"
	@echo "Spark Master:    http://localhost:9090"
	@echo "History Server:  http://localhost:18080"
	@echo "Spark app UI:    http://localhost:4040"

# Taxi / full CDC downloads: next sessions (scripts removed for this lesson).
