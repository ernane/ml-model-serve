API_NAME="ml-model-serve-api"

# verifying which docker compose command is available
ifneq (, $(shell which docker-compose))
    DOCKER_COMPOSE = docker-compose
else ifneq (, $(shell which docker))
    DOCKER_COMPOSE = docker compose
else
    $(error "Neither docker-compose nor docker compose is available")
endif

############################################
# COMMANDS TO RUN USING DOCKER (RECOMMENDED)
############################################

docker/install: 
	$(DOCKER_COMPOSE) build ${API_NAME}

docker/lint:
	$(DOCKER_COMPOSE) run ${API_NAME} poetry run task lint

docker/test:
	$(DOCKER_COMPOSE) AWS_DEFAULT_REGION=us-east-1 run ${API_NAME} poetry run task test