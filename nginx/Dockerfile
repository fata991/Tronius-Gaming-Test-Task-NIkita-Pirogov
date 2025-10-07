# Start from the official lightweight Nginx base image.
FROM nginx:stable-alpine

# Remove the default Nginx configuration file.
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom nginx.conf to the container's configuration directory.
COPY nginx.conf /etc/nginx/conf.d/default.conf
