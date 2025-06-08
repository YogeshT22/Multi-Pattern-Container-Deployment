# Use an official Nginx image as the base image.
# 'alpine' is a very small, lightweight version, which is great practice.
FROM nginx:alpine

# Copy our simple index.html file into the directory where Nginx looks for files to serve.
# The destination path `/usr/share/nginx/html` is a standard path inside the Nginx container.
COPY ./index.html /usr/share/nginx/html
