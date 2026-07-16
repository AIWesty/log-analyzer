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


ruff: 
	poetry run ruff check src/ tests/

ruffix:
	poetry run ruff check src/ tests/ --fix

ruff-format:
	poetry run ruff format .
	
prepare:
	cd ansible && ansible-playbook playbooks/prepare-host.yml -i inventory.ini -v

# Деплой приложения
deploy:
	cd ansible && ansible-playbook playbooks/deploy.yml \
		-i inventory.ini \
		--extra-vars "docker_tag=latest" \
		--extra-vars "registry_user=token" \
		--extra-vars "registry_password=$(shell cat ~/.github_token)" \
		-v

# Dry-run (показать что изменится без применения)
deploy-dry:
	cd ansible && ansible-playbook playbooks/deploy.yml \
		-i inventory.ini \
		--check --diff -v

# Проверить SSH
test-ssh:
	ssh -i ~/.ssh/deploy_key deployer@192.168.1.100 "echo '✅ SSH works' && hostname && docker --version"

# Ping all hosts
check:
	cd ansible && ansible all -i inventory.ini -m ping