# Automated Web Server Deployment

A complete and repeatable workflow for deploying a secure, containerized web application using Docker, Nginx, and Python on a fresh Ubuntu server.

---

## Key Features

* **Fully Automated Setup**: A single script installs all necessary dependencies, including Docker and Docker Compose.
* **Containerized Environment**: Docker ensures that the application and its environment are isolated, consistent, and portable.
* **Secure by Design**: Nginx is used as a reverse proxy to handle incoming HTTPS traffic, terminating SSL/TLS before forwarding requests to the application.
* **Simplified Management**: A `Makefile` provides simple, one-word commands like `deploy`, `test`, and `clean` to manage the entire application lifecycle.

---

## Architecture

At its core, the project employs a standard reverse proxy pattern. An Nginx container serves as the secure, public-facing entry point, while the Flask application runs in a separate container on a private Docker network.

---

## Getting Started

Follow these instructions on a clean machine to get the application running.

### Prerequisites

* A Linux-based host machine (tested on **Ubuntu 24.04**).
* **Git** for cloning the repository.

### Installation and Deployment

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/fata991/Tronius-Gaming-Test-Task-NIkita-Pirogov.git]
    cd Tronius-Gaming-Test-Task-NIkita-Pirogov/
    ```

2.  **Run the Setup Script**
    This one-time script installs all system dependencies.
    ```bash
    # This command requires administrator privileges
    sudo ./scripts/setup_vm.sh
    ```
    > **IMPORTANT**: You must **log out and log back in** for the system changes to take effect before proceeding to the next step.

3.  **Deploy the Application**
    After logging back in, navigate to the project directory and run the deploy command. This will generate certificates, build the Docker images, and start the services.
    ```bash
    make deploy
    ```

---

## Usage

The `Makefile` simplifies all common operations.

* `make deploy`
    * Builds and starts the Nginx and Flask containers. The primary command to run the application.
* `make test`
    * Runs an automated test suite to verify that the deployment is successful and the services are responsive.
* `make clean`
    * Stops and removes all containers, images, and certificates associated with the project.
* `make build`
    * Builds the Docker images without starting the containers. This is automatically part of `make deploy`.
