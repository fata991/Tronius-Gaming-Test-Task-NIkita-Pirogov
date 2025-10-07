# Start from an official, lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# --- Production & Security Enhancements ---
# 1. Create a dedicated group and user to run the application
RUN addgroup --system app && adduser --system --group app

# 2. Switch to the new unprivileged user
USER app
# --- End Enhancements ---

# Expose port 5000 to allow traffic from the Docker network
EXPOSE 5000

# Define the command to run when the container starts
# Use Gunicorn as the production-ready WSGI server
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]
