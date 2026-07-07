.PHONY: build run test analyze clean


build: 
	docker build -t log-analyzer:latest .

run: 
	docker compose up -d 

analyz: 
	docker compose run --rm log-analyzer

test: 
	pytest --cov=src --cov-report=term-missing

generate-traffic:
	./scripts/generate_traffic.sh 100

clean:
	docker-compose down -v
	docker system prune -f

logs:
	docker-compose logs -f

shell:
	docker-compose exec nginx sh

black:
	poetry run black --check .

blackfix:
	poetry run black .

ruff: 
	poetry run ruff check src/ tests/

ruffix:
	poetry run ruff check src/ tests/ --fix