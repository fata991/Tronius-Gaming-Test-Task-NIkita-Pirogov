#!/bin/bash

# This script serves as a convenient wrapper for the test.py script.
# It automatically detects the machine's primary IP address and passes
# it to the test script, removing the need for manual input.

echo "[*] Automatically detecting the server's IP address..."

# Get the IP address and select the first one in the list.
# 'hostname -I' can return multiple IPs; 'awk' grabs the first one.
SERVER_IP=$(hostname -I | awk '{print $1}')

# Check if an IP address was actually found.
if [ -z "$SERVER_IP" ]; then
    echo "❌ FAILED: Could not automatically determine the IP address."
    exit 1
fi

echo "[+] IP address detected: $SERVER_IP"
echo "[*] Now running the Python test suite..."

# Execute the main test script, passing the detected IP as an argument.
./scripts/test.py "$SERVER_IP"
