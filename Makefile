.PHONY: all run clean test

# Define the default target
all: build

# Define the target to build the Docker images
build:
	docker-compose up 

# Define the target to run the Docker containers
run:
	docker-compose up --build

# Define the target to clean up Docker resources
clean:
	docker-compose down

# Define a target to run the tests
test:
	# Add commands to run your tests here
      pytest tests/