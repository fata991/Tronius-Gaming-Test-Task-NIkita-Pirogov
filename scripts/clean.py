#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil

# --- Configuration ---
CERT_DIR = "nginx/ca"

def run_command(command):
    """Runs a shell command and checks for errors."""
    try:
        print(f"[*] Running command: {' '.join(command)}")
        subprocess.run(command, check=True, text=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        # We don't treat "not found" errors from 'down' as failures, just warnings.
        if "not found" in e.stderr.lower():
            print(f"[*] INFO: Some resources were already gone (this is normal).")
            return True
        print(f"[!] ERROR: Command failed with exit code {e.returncode}")
        print(f"    Command: {' '.join(command)}")
        print(f"    Stderr:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"[!] ERROR: Command not found. Is docker-compose installed?")
        return False

def remove_certs():
    """Removes the certificate directory if it exists."""
    # Construct the full path relative to the script's location
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.join(script_dir, '..')
    cert_path = os.path.join(project_root, CERT_DIR)

    if os.path.exists(cert_path):
        print(f"[*] Removing certificate directory: {cert_path}")
        try:
            shutil.rmtree(cert_path)
            return True
        except OSError as e:
            print(f"[!] ERROR: Failed to remove directory {cert_path}. Error: {e}")
            print(f"    You may need to remove it manually with 'sudo rm -rf {cert_path}'")
            return False
    else:
        print("[*] Certificate directory not found, skipping.")
        return True

def main():
    """Main function to clean the Docker environment and certificates."""
    print("[*] Starting the total cleanup process...")
    
    cleanup_command = ["docker-compose", "down", "--rmi", "all", "-v"]
    
    docker_cleaned = run_command(cleanup_command)
    certs_cleaned = remove_certs()
    
    if docker_cleaned and certs_cleaned:
        print("\n" + "="*30)
        print("✅ SUCCESS: Total cleanup complete!")
        print("="*30)
        sys.exit(0)
    else:
        print("\n" + "="*30)
        print("❌ FAILED: Cleanup process encountered one or more errors.")
        print("="*30)
        sys.exit(1)

if __name__ == "__main__":
    main()
