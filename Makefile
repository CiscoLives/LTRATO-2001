.DEFAULT_GOAL := help

.PHONY: help
help:	## Show this help
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:  ## Build Docker images for this application
	[ -f .env ] || cp .env-template .env
	docker-compose -f docker-compose.yaml build $(s)

.PHONY: down
down:	## Stop application, remove containers and networks
	docker-compose -f docker-compose.yaml down
	@echo "Django App has been stopped!"

.PHONY: run
run: build ## Run development environment
	docker-compose -f docker-compose.yaml up -d
	@echo "Django App is now running!"

.PHONY: restart
restart:	## Restart services
	docker-compose -f docker-compose.yaml restart $(s)

.PHONY: destroy-all
destroy-all:	## Stop application, remove containers, networks, images and volumes
	docker-compose -f docker-compose.yaml down -v --rmi all
	@echo "Django App has been successfully uninstalled!"

.PHONY: destroy-volumes
destroy-volumes:	## Stop application, remove containers, networks and VOLUMES
	docker-compose -f docker-compose.yaml down -v
	@echo "Docker volumes were successfully removed !"

.PHONY: destroy-images
destroy-images:	## Stop application, remove containers, networks and IMAGES
	docker-compose -f docker-compose.yaml down --rmi all
	@echo "Docker images were successfully removed !"

.PHONY: logs
logs:	## View output from containers
	docker-compose -f docker-compose.yaml logs -f $(s)

.PHONY: ps
ps:	## List containers
	docker-compose -f docker-compose.yaml ps

.PHONY: images
images: ## List App Docker images
	docker-compose -f docker-compose.yaml images

.PHONY: migrate
migrate: ## Run Django ./manage.py migrate 

	docker-compose -f docker-compose.yaml exec -T app python manage.py migrate

.PHONY: migrations
migrations: ## Run Django ./manage.py makemigrations 

	docker-compose -f docker-compose.yaml exec -T app python manage.py makemigrations
