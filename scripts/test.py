#!/usr/bin/env python3

import requests
import sys
import urllib3
import socket
import ssl
import subprocess

# --- Configuration (Defaults) ---
DOMAIN = "myservice.example.com"
EXPECTED_TEXT = "Hello, World!"
EXPECTED_ISSUER_CN = "MyPrivateCA"

# --- Helper Functions ---
def print_success(message):
    print(f"✅ SUCCESS: {message}")

def print_failure(message):
    print(f"❌ FAILED: {message}")
    sys.exit(1)

def print_step(message):
    print("\n" + "="*15 + f" {message} " + "="*15)

# --- Test Functions ---
def test_http_redirect(server_ip):
    http_url = f"http://{server_ip}/"
    print_step("TEST 1: HTTP Redirect")
    print(f"[*] Making request to {http_url}...")
    try:
        response = requests.get(http_url, headers={'Host': DOMAIN}, timeout=5, allow_redirects=False)
        if response.status_code == 301:
            print_success(f"Received correct status code (301 Moved Permanently).")
        else:
            print_failure(f"Expected status code 301, but got {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print_failure(f"Could not connect to the HTTP endpoint. Error: {e}")

def test_https_content(server_ip):
    https_url = f"https://{server_ip}/"
    print_step("TEST 2: HTTPS Content")
    print(f"[*] Making request to {https_url}...")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        response = requests.get(https_url, headers={'Host': DOMAIN}, verify=False, timeout=5)
        response.raise_for_status()
        print_success("Received successful HTTP status code (200 OK).")
        if EXPECTED_TEXT in response.text:
            print_success(f"Response content is correct (Found '{EXPECTED_TEXT}').")
        else:
            print_failure(f"Expected text '{EXPECTED_TEXT}' not found in response.")
    except requests.exceptions.RequestException as e:
        print_failure(f"Could not connect to the HTTPS endpoint. Error: {e}")

def test_certificate_issuer(server_ip):
    print_step("TEST 3: Certificate Issuer")
    print(f"[*] Inspecting SSL certificate from {server_ip} via openssl...")

    command = (
        f"openssl s_client -showcerts -servername {DOMAIN} -connect {server_ip}:443 < /dev/null 2>/dev/null | "
        f"openssl x509 -noout -issuer | "
        f"sed -n 's/.*CN = //p'"
    )
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10, check=True)
        issuer_cn = result.stdout.strip()

        if issuer_cn == EXPECTED_ISSUER_CN:
            print_success(f"Certificate issuer is correct ('{EXPECTED_ISSUER_CN}').")
        else:
            print_failure(f"Expected issuer CN '{EXPECTED_ISSUER_CN}', but got '{issuer_cn}'.")
    except subprocess.CalledProcessError as e:
        print_failure(f"The openssl command failed. Is openssl installed?\nError: {e.stderr}")
    except Exception as e:
        print_failure(f"An unexpected error occurred. Error: {e}")

# --- Main Execution ---
def main():
    if len(sys.argv) != 2:
        print("Usage: ./test.py <SERVER_IP_ADDRESS>")
        print("Example: ./test.py 192.168.0.20")
        sys.exit(1)
    server_ip = sys.argv[1]
    test_http_redirect(server_ip)
    test_https_content(server_ip)
    test_certificate_issuer(server_ip)
    print("\n" + "="*20 + " ALL TESTS PASSED " + "="*20)

if __name__ == "__main__":
    main()
