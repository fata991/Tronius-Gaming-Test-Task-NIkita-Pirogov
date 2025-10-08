# Automated Web Server Deployment

A completem automated and repeatable workflow for deploying a secure, containerized web application using Docker, Nginx, and Python on a fresh Ubuntu server.

---


# Overview

This repository is a solution to a DevOps task requiring the build and deploy of a simple web server. The goal was not just to create a functional deployment, but to build a robust and secure system that reflects modern DevOps principles.

The entire lifecycle of the application (deployment, testing, and cleanup) is managed through a simple `Makefile` that orchestrates a suite of automation scripts.

## Key Features

* **Fully Automated Setup**: Prior to the usage of `Make` setup_vm bash script installs all necessary dependencies, including Docker and Docker Compose. Some scripts are in Python, just to show that I can make them as well. My preference is still bash due to having the much more experience with it. 
* **Containerized Environment**: Docker ensures that the application and its environment are isolated, consistent, and portable.
* **Secure by Design**: Nginx is used as a reverse proxy to handle incoming HTTPS traffic, terminating SSL/TLS before forwarding requests to the application.
* **Simplified Management**: A `Makefile` provides simple, one-word commands like `build`, `deploy`, `test`, and `clean` to manage the entire application lifecycle.

---

## Architecture and Design Decisions

Nginx (Reverse Proxy): Acts as the public-facing gateway. Nginx was chosen mostly because it is an industry standart with high performance and stability. Capabilities as a reverse proxy and SSL/TLS termination point. Isolating the application server from direct exposure to the internet.

Flask Application (Gunicorn): The Python web server runs in a separate, isolated container. The application is served by Gunicorn, a production-grade WSGI server, instead of Flask's built-in development server. This ensures the application can handle concurrent requests and is suitable for a production environment.

Docker Network: Docker Compose creates an isolated network for the containers, allowing nginx and app to communicate securely by their service names.

At its core, the project employs a standard reverse proxy pattern. An Nginx container serves as the secure, public-facing entry point, while the Flask application runs in a separate container on a private Docker network.

---

## Automation

Makefile Interface: A Makefile provides a simple, unified, and standard interface for all lifecycle operations (build, deploy, test, clean). This abstracts away the complexity of the underlying scripts.

Testing: A  test suite (test.py) validates the HTTP redirect, HTTPS content, and the SSL certificate's issuer.

Continuous Integration (CI): A GitHub Actions workflow automatically runs linting and build checks on every push and pull request, ensuring code quality and preventing broken changes from being merged.

---

## Getting Started

Follow these instructions on a clean Ubuntu 24.04 machine to get the application running.

### Prerequisites

* A Linux-based host machine (tested on **Ubuntu 24.04**). Since I don't have any access to MacOS devices I couldn't test it fully, but it should work. 
* **Git** for cloning the repository. Already installed on Ubuntu but still.

### Installation and Deployment

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/fata991/Tronius-Gaming-Test-Task-NIkita-Pirogov.git
    cd Tronius-Gaming-Test-Task-NIkita-Pirogov/
    ```

2.  **Run the Setup Script**
    This one-time script installs all system dependencies. This script basically installed all the needed packages and dependencies so it is ready to run Dockerized projects. It installs Docker, Docker Compose,   and setts up the firewall securely. usermod -aG docker $CURRENT_USER adds current user to the docker group, which allows running docker commands without sudo.
    ```bash
    # This command requires administrator privileges
    sudo ./scripts/setup_vm.sh
    ```
    > **IMPORTANT**: You must **log out and log back in** for the system changes to take effect before proceeding to the next step.

3.  **Deploy the Application**
    So, I could have added multi stage build and caching to speed up the process of creating docker images but since it takes only 40 seconds to make deployment it is redundant. 
    After logging back in, navigate to the project directory and run the deploy command. This will generate certificates, build the Docker images, and start the services. 
    ```bash
    make deploy
    ```

---

## Usage

The `Makefile` simplifies all common operations.

* `make build`
    * Builds the Docker images without starting the containers. This is automatically part of `make deploy`.

* `make deploy`
    * Builds and starts the Nginx and Flask containers. The primary command to run the application.
* `make test`
    * Runs an automated test suite to verify that the deployment is successful and the services are responsive.
* `make clean`
    * Stops and removes all containers, images, and certificates associated with the project.
