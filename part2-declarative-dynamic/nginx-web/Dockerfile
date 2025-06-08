# Use an official Nginx image as the base image.
FROM nginx:alpine

# Install the AWS CLI tool. 'apk' is the package manager for Alpine Linux.
RUN apk add --no-cache aws-cli

# Copy our entrypoint script from the 'scripts' folder (which is inside the build context)
# into the root of the container's filesystem.
COPY scripts/entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable. This is a critical step.
RUN chmod +x /entrypoint.sh

# Set the entrypoint script as the command to run when the container starts.
ENTRYPOINT ["/entrypoint.sh"]