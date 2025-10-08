#!/bin/bash

# This script automates the creation of a private Certificate Authority (CA)
# and a server certificate signed by that CA. It is idempotent and will not
# overwrite existing certificates.

# --- Configuration ---
CERT_DIR="nginx/ca"
CA_KEY="$CERT_DIR/ca.key"
CA_CERT="$CERT_DIR/ca.crt"
SERVER_KEY="$CERT_DIR/myservice.example.com.key"
SERVER_CSR="$CERT_DIR/myservice.example.com.csr"
SERVER_CERT="$CERT_DIR/myservice.example.com.crt"
DAYS_VALID=365
DOMAIN="myservice.example.com"

# --- Main Logic ---

# Check if the final server certificate already exists.
if [ -f "$SERVER_CERT" ]; then
    echo "✅ Certificates already exist. No action taken."
    exit 0
fi

echo "[*] No existing certificates found. Starting generation process..."

# Create the directory for certificates.
mkdir -p $CERT_DIR
echo "[+] Created directory: $CERT_DIR"

# 1. Create the Certificate Authority (CA)
echo "[*] Generating private CA key..."
openssl genrsa -out "$CA_KEY" 2048

echo "[*] Generating self-signed CA root certificate..."
openssl req -x509 -new -nodes -key "$CA_KEY" -sha256 -days $DAYS_VALID -out "$CA_CERT" -subj "/C=US/ST=State/L=City/O=MyPrivateCA/OU=DevOps/CN=MyPrivateCA"

# 2. Create the Server Certificate
echo "[*] Generating server private key..."
openssl genrsa -out "$SERVER_KEY" 2048

echo "[*] Generating Certificate Signing Request (CSR) for $DOMAIN..."
openssl req -new -key "$SERVER_KEY" -out "$SERVER_CSR" -subj "/C=US/ST=State/L=City/O=MyService/OU=Web/CN=$DOMAIN"

# 3. Sign the Server Certificate with the CA
echo "[*] Signing the server certificate with our private CA..."
openssl x509 -req -in "$SERVER_CSR" -CA "$CA_CERT" -CAkey "$CA_KEY" -CAcreateserial -out "$SERVER_CERT" -days $DAYS_VALID -sha256

echo ""
echo "=============================================="
echo "✅ SUCCESS: All certificates generated."
echo "=============================================="

