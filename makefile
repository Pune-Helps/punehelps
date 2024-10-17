# Makefile

# Variables
DOCKER_IMAGE = flaskapp
DOCKER_TAG = latest
DOCKER_CONTAINER = flaskapp

.PHONY: build run stop clean logs

# Build the Docker image
build:
	sudo docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

# Run the Docker container
run:
	sudo docker run -p 5000:5000 --name $(DOCKER_CONTAINER) -d $(DOCKER_IMAGE):$(DOCKER_TAG)

# Stop the running container
stop:
	sudo docker stop $(DOCKER_CONTAINER) || true
	sudo docker rm $(DOCKER_CONTAINER) || true

# Remove the Docker image
clean:
	sudo docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG) || true

# Show logs of the running container
logs:
	sudo docker logs -f $(DOCKER_CONTAINER)
