#!/usr/bin/env python3

import requests
import sys
import urllib3

# --- Configuration ---
SERVER_IP = "192.168.0.19"
DOMAIN = "myservice.example.com"
URL = f"https://{SERVER_IP}/"
EXPECTED_TEXT = "Hello, World!"

def run_test():
    """
    Runs an automated test to check if the web server is responding correctly.
    """
    print(f"[*] Testing connection to {URL} (for domain {DOMAIN})...")

    # This line suppresses the security warning for using a self-signed certificate.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        # The 'headers' trick the server into thinking we are a browser asking for the correct domain.
        # The 'verify=False' tells the script to trust our custom self-signed certificate.
        response = requests.get(URL, headers={'Host': DOMAIN}, verify=False, timeout=10)

        # Check 1: Did we get a successful status code (like 200 OK)?
        response.raise_for_status()
        print("[+] HTTP Status Code: OK")

        # Check 2: Does the webpage contain the "Hello, World!" text?
        if EXPECTED_TEXT in response.text:
            print(f"[+] Response Content: OK (Found '{EXPECTED_TEXT}')")
        else:
            print(f"[!] FAILED: Expected text not found in the response.")
            sys.exit(1)

        print("\n" + "="*30)
        print("✅ SUCCESS: The web server is deployed and running correctly!")
        print("="*30)
        sys.exit(0)

    except requests.exceptions.RequestException as e:
        print(f"\n[!] FAILED: Could not connect to the server.")
        print(f"    Error details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
