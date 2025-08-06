# --------------------------------
# Purpose: Dockerfile for Nginx web server with AWS CLI
# Target: Simulating Cloud with Docker + LocalStack
# This is personal work for educational purposes.
# --------------------------------

FROM nginx:alpine
RUN apk add --no-cache aws-cli

COPY scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
