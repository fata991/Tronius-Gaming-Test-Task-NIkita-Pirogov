# Start from an official, lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
# This is done first to leverage Docker's layer caching. 
# The dependencies are only re-installed if requirements.txt changes.
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 to allow traffic to the container from the Docker network
EXPOSE 5000

# Define the command to run when the container starts
CMD ["python", "app.py"]
