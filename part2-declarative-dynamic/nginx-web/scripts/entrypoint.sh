#!/bin/sh

set -e
echo "Fetching website content from S3..."


# Dev note: the --endpoint-url flag is used to target LocalStack.
aws s3 cp s3://${S3_BUCKET_NAME}/index.html /usr/share/nginx/html/index.html --endpoint-url=${S3_ENDPOINT_URL}

echo "Content fetched successfully. Starting Nginx..."

# Dev note: 'exec' is important because it replaces the shell process with the Nginx process,
# allowing it to receive signals from Docker correctly (like when you run 'docker stop').

exec nginx -g 'daemon off;'
