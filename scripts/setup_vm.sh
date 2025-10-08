#!/bin/bash

# This script prepares a bare Ubuntu VM to run the project by installing
# all necessary dependencies like Docker and Docker Compose.
# It should be run with sudo privileges.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "[*] Starting environment setup..."

# --- 1. System Update and Prerequisite Installation ---
echo "[+] Updating package list and installing prerequisites..."
apt-get update
apt-get install -y ca-certificates curl

# --- 2. Install Docker Engine ---
echo "[+] Installing Docker Engine..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin

# --- 3. Install Docker Compose ---
echo "[+] Installing Docker Compose..."
DOCKER_COMPOSE_VERSION="v2.27.0" # Use a specific version for consistency
curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# --- 4. Add User to Docker Group (Optional but Recommended) ---
# This allows running docker commands without sudo.
# The user will need to log out and log back in for this to take effect.
CURRENT_USER=$(logname)
echo "[+] Adding current user ('$CURRENT_USER') to the 'docker' group..."
usermod -aG docker $CURRENT_USER

# --- 5. Configure Firewall (UFW) ---
echo "[+] Configuring firewall to allow SSH, HTTP, and HTTPS..."
ufw allow ssh
ufw allow http
ufw allow https
ufw --force enable

echo ""
echo "=================================================================="
echo "✅ SUCCESS: Environment setup is complete."
echo "IMPORTANT: Please log out and log back in to apply group changes."
echo "=================================================================="

