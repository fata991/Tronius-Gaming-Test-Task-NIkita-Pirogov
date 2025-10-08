Web Server Deployment Project
A complete, automated workflow for deploying a secure, containerized web application using Docker, Nginx, and Python. This project is designed to be fully repeatable on a fresh Ubuntu machine.

Architecture
This project uses a standard reverse proxy pattern. An Nginx container acts as the secure, public-facing entry point, terminating SSL and forwarding traffic to a backend Flask application container running on a private Docker network.

+-----------------+      +------------------------+      +---------------------+
|   User/Client   |----->|     Nginx Container    |----->|   Flask App         |
| (HTTPS Request) |      | (Port 443, SSL/TLS)    |      |   Container         |
+-----------------+      +------------------------+      +---------------------+

Prerequisites
A Linux-based host machine (tested on Ubuntu 24.04).

git to clone the repository.

Quick Start & Usage
Follow these steps in order on a new, clean machine.

1. Clone the Repository
git clone [https://github.com/fata991/Tronius-Gaming-Test-Task-NIkita-Pirogov.git](https://github.com/fata991/Tronius-Gaming-Test-Task-NIkita-Pirogov.git)
cd Tronius-Gaming-Test-Task-NIkita-Pirogov/

2. Run the Environment Setup Script
This script must be run once to install all dependencies, including Docker, Docker Compose, and make.

# This command requires administrator privileges
sudo ./scripts/setup_vm.sh

IMPORTANT: After the script completes, you must log out and log back in for the user permission changes to take effect.

3. Use make to Manage the Application
After re-logging in and navigating back to the project directory, use the following commands:

Build the Docker Images (Optional)
This step is automatically included in make deploy, but can be run separately.

make build

Deploy the Application
This command generates certificates, builds images (if needed), and starts the application.

make deploy

Test the Deployment
Run the automated test suite to verify everything is working correctly.

make test

Clean the Environment
Stop and remove all containers, images, and certificates.

make clean
