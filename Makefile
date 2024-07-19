# Variables
DOCKER_COMPOSE = docker-compose
DOCKER = docker
SERVER_DIR = ./LoadBalancer
LOAD_BALANCER_DIR = ./LoadBalancer
SERVER_IMAGE = simple-server
LOAD_BALANCER_IMAGE = load-balancer
CONTAINER_NAME = load-balancer

# Targets
all: build up

build:
	@echo "Building Docker images..."
	$(DOCKER) build -t $(SERVER_IMAGE) $(SERVER_DIR)
	$(DOCKER) build -t $(LOAD_BALANCER_IMAGE) $(LOAD_BALANCER_DIR)

up:
	@echo "Starting containers..."
	$(DOCKER_COMPOSE) up -d

down:
	@echo "Stopping containers..."
	$(DOCKER_COMPOSE) down

logs:
	@echo "Viewing logs..."
	$(DOCKER_COMPOSE) logs -f

clean:
	@echo "Removing containers and images..."
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

# adding servers
add-server:
	@echo "Adding server..."
	$(DOCKER_COMPOSE) up --scale server=3

