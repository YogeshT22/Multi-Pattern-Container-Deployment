import docker

CONTAINER_NAME = 'py-web-server'
NETWORK_NAME = 'py-web-net'

client = docker.from_env()

print("--- Starting Cleanup Script ---")
try:
    container = client.containers.get(CONTAINER_NAME)
    print("Stopping and removing container...")
    container.stop()
    container.remove()
    print("Container removed.")
except docker.errors.NotFound:
    print("Container not found.")

try:
    network = client.networks.get(NETWORK_NAME)
    print("Removing network...")
    network.remove()
    print("Network removed.")
except docker.errors.NotFound:
    print("Network not found.")

print("--- Cleanup Complete ---")
