# --------------------------------
# Purpose: Imperative deployment script for a local web server using Docker
# Target: Simulating Cloud with Docker + LocalStack
# This is personal work for educational purposes.
# --------------------------------

import docker
import os

# Dev note: using absolute path for the content directory to avoid issues
CONTENT_PATH = os.path.join(os.path.abspath('.'), 'web-content')
CONTAINER_NAME = 'py-web-server'
NETWORK_NAME = 'py-web-net'
IMAGE_NAME = 'ubuntu:20.04'

print("--- Starting Imperative Deployment Script ---")

# Initialize Docker Client
client = docker.from_env()
print("Docker client initialized.")

# Cleanup old resources (makes the script re-runnable)
print(f"Checking for existing container named '{CONTAINER_NAME}'...")
try:
    old_container = client.containers.get(CONTAINER_NAME)
    print("Found existing container. Stopping and removing it.")
    old_container.stop()
    old_container.remove()
    print("Old container removed.")
except docker.errors.NotFound:
    print("No existing container found. Good to go.")

# Network Setup
print(f"Checking for existing network named '{NETWORK_NAME}'...")
try:
    network = client.networks.get(NETWORK_NAME)
    print("Network already exists.")
except docker.errors.NotFound:
    print("Network not found. Creating it now.")
    network = client.networks.create(NETWORK_NAME, driver='bridge')
    print(f"Network '{NETWORK_NAME}' created.")


# Run the "EC2" Container (from a base Ubuntu image)
print(
    f"Starting a new container '{CONTAINER_NAME}' from image '{IMAGE_NAME}'...")

# Dev note: A base ubuntu container will exit immediately if it has no running process.
# Dev note: 'sleep 3600' to keep it alive so we can exec commands into it.

container = client.containers.run(
    image=IMAGE_NAME,
    name=CONTAINER_NAME,
    detach=True,          # Run in the background (detached mode)
    ports={'80/tcp': 8081},  # Map container port 80 to host port 8081
    network=network.name,
    volumes={
        CONTENT_PATH: {'bind': '/var/www/html', 'mode': 'rw'}
    },
    command="sleep 3600"  # Keep the container running
)
print(f"Container '{container.name}' started with ID: {container.short_id}")

# Provision the Container (Install Nginx)
print("Provisioning container: Installing Nginx...")

update_result = container.exec_run("sh -c 'apt-get update'", tty=False)
if update_result.exit_code != 0:
    print("Error: apt-get update failed!")
    print(update_result.output.decode())
    container.stop()
    container.remove()
    exit()

install_result = container.exec_run(
    "sh -c 'DEBIAN_FRONTEND=noninteractive apt-get install -y nginx'",
    tty=False
)
if install_result.exit_code != 0:
    print("Error: Nginx installation failed!")
    print(install_result.output.decode())
    container.stop()
    container.remove()
    exit()
print("Nginx installed successfully.")


print("Starting Nginx service inside the container...")
start_cmd_result = container.exec_run(
    "service nginx start", tty=False, detach=True)

# Dev note: We don't check the exit code here as the service starts in the background

print("\n--- Deployment Complete! ---")
print(f"Your website should be available at: http://localhost:8081")
print(
    f"To stop and remove the container, run: docker stop {CONTAINER_NAME} && docker rm {CONTAINER_NAME}")
