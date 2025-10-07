# Makefile for managing the deployment lifecycle of the web server project.
# Provides a clean, unified interface for all common tasks.

# This tells 'make' that these are command names, not files to be built.
.PHONY: all setup certs build deploy clean test

# Default command to run if you just type 'make'.
# It will build, deploy, and then test the application.
all: build deploy test

# Target to set up the host machine with all necessary dependencies.
setup:
	@echo "--- Setting up VM (requires sudo password) ---"
	@sudo ./scripts/setup_vm.sh

# Target to generate the self-signed certificates. This is idempotent.
certs:
	@echo "--- Generating SSL Certificates ---"
	@./scripts/generate_certs.sh

# Target to build the Docker images for all services.
build:
	@echo "--- Building Docker Images ---"
	@./scripts/build.py

# Target to deploy the application stack in the background.
# Note: It depends on the 'certs' target, so it will automatically
# generate certificates if they are missing before deploying.
deploy: certs
	@echo "--- Deploying Application Stack ---"
	@./scripts/deploy.py

# Target to stop and completely remove the application stack and images.
clean:
	@echo "--- Cleaning Environment ---"
	@./scripts/clean.py

# Target to run the automated test suite.
test:
	@echo "--- Running Automated Tests ---"
	@./scripts/run_tests.sh
