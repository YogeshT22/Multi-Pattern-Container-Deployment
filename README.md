# Mini Project 1: Multi-Pattern Containerized Web Server Deployment

This project demonstrates foundational DevOps principles by deploying an Nginx web server using three distinct, progressively complex patterns. It uses Docker, Docker Compose, Python, and LocalStack to simulate a real-world cloud environment on a local machine, showcasing a journey from basic containerization to advanced, programmatic automation.

---

## Core Concepts Demonstrated

- **Infrastructure as Code (IaC):** Implemented both **declarative** (Docker Compose) and **imperative** (Python script) approaches, highlighting the trade-offs of each.
- **Containerization & Orchestration:** Created custom, multi-stage Docker images and managed a multi-container application stack with Docker Compose.
- **Cloud Services Simulation:** Leveraged LocalStack to mimic AWS S3 for dynamic content hosting, enabling development and testing of cloud-native patterns without an AWS account.
- **Automation & Scripting:** Developed a Python script using the Docker SDK (`docker-py`) to programmatically manage the entire application lifecycle, from network creation to container provisioning and cleanup.
- **Decoupled Architecture:** Refactored a monolithic application into a dynamic system where the web server fetches its content from an object store (S3) on startup via a custom entrypoint script.
- **Configuration Management:** Utilized environment variables to pass configuration (API endpoints, credentials, bucket names) into containers, following Twelve-Factor App principles.
- **Container Networking:** Configured service-to-service communication between containers on a user-defined Docker network.

---

## Technologies Used

- **Containerization:** Docker, Docker Compose
- **Cloud (Simulated):** LocalStack (emulating AWS S3)
- **Automation:** Python 3, Docker SDK (`docker-py`), Bash Scripting
- **Web Server:** Nginx
- **CLI Tools:** AWS CLI

---

## Project Structure & How to Run

This repository is divided into three parts, each located in its own directory and representing a different deployment pattern.

### Part 1: Basic Declarative Deployment

A simple, self-contained Nginx deployment where the website content is built directly into the Docker image.

📦 _Teaches you how to build a static web server using Docker Compose only._

**To Run:**

```bash
cd part1-declarative-basic
docker-compose up -d

```

Access the site at <http://localhost:8080>

### Part 2: Dynamic Declarative Deployment

An advanced pattern where the Nginx container is generic and dynamically fetches its index.html file from a LocalStack S3 bucket on startup.

🔁 _Demonstrates dynamic content loading using S3 + environment configs._

**To Run:**

#### First, start LocalStack and provision the S3 bucket

```bash
cd part2-declarative-dynamic
docker-compose up -d localstack
```

#### Confirm LocalStack is running

```bash
docker logs -f local-aws-cloud
```

Wait for it to say Ready. or similar with no repeated crash logs.

> ℹ️ Once LocalStack shows "Ready" in the logs, press `Ctrl + C` to exit log view, then proceed with the AWS CLI commands below.

#### Use the AWS CLI to create the bucket and upload the content

> 💡 **Note:** Ensure AWS CLI is configured with dummy credentials:
> `Access Key ID: test`, `Secret Access Key: test`, `Region: us-east-1`
> You can run `aws configure` to set these.

```bash
aws configure
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-dynamic-website-bucket
aws --endpoint-url=http://localhost:4566 s3 cp ./nginx-web/index.html s3://my-dynamic-website-bucket/
```

#### Now, start the web server, which will pull its content from S3

```bash

docker-compose up -d nginx-service
```

Access the site at <http://localhost:8080>

#### To stop and clean up Part 2 containers

```bash
docker-compose down
```

### Part 3: Imperative Deployment with Python

A Python script that uses the Docker SDK to build the entire environment from scratch. This script handles network creation, container provisioning (installing Nginx inside a bare Ubuntu container), and deployment.

⚙️ _Automates everything using Python + Docker SDK (full control over containers)._

**To Run:**

```bash
cd part3-imperative-python
```

#### Install the required Python library

```bash
pip install docker
```

#### Run the deployment script

```bash
python3 deploy.py
```

Access the site at <http://localhost:8081>.

#### To clean up

```bash

python3 cleanup.py
```

### Architectural Diagram (Part 2: Dynamic Deployment)

This diagram illustrates the dynamic content flow, where the Nginx container is decoupled from its content.

![Architecture Diagram](./src/architecture-diagram.png)

## Troubleshooting

### LocalStack crashes with `/tmp/localstack` error

This is a known issue on some systems (especially Windows) when mounting the host's `/tmp` directory into LocalStack.
**Fix:** Use a Docker-managed named volume and set `TMPDIR=/tmp/localstack-custom` in your `docker-compose.yml`.

### AWS CLI fails to connect to `localhost:4566`

Ensure LocalStack container is running:

```bash
docker ps
docker logs local-aws-cloud
```

### If it’s not running, fix the volume issue or use manual method

```bash
docker run -d -e SERVICES=s3 -e TMPDIR=/tmp/localstack-custom \
  -v localstack_data:/tmp/localstack-custom -p 4566:4566 \
  --name local-aws-cloud localstack/localstack:latest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
