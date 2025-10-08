#!/usr/bin/env python3

import subprocess
import sys

def run_command(command):
    """Runs a shell command and checks for errors."""
    try:
        print(f"[*] Running command: {' '.join(command)}")
        subprocess.run(command, check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] ERROR: Command failed with exit code {e.returncode}")
        print(f"    Command: {' '.join(command)}")
        print(f"    Output:\n{e.stdout}\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"[!] ERROR: Command not found. Is docker-compose installed and in your PATH?")
        return False

def main():
    """Main function to build the Docker images."""
    print("[*] Starting the build process...")
    
    build_command = ["docker-compose", "build"]
    
    if run_command(build_command):
        print("\n" + "="*30)
        print("✅ SUCCESS: Docker images built successfully!")
        print("="*30)
        sys.exit(0)
    else:
        print("\n" + "="*30)
        print("❌ FAILED: Build process encountered an error.")
        print("="*30)
        sys.exit(1)

if __name__ == "__main__":
    main()
