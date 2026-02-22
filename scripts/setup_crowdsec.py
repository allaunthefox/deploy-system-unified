#!/usr/bin/env python3
import subprocess
import json
import os
import sys

BOUNCER_CONFIG = "/etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml"
CONTAINER_NAME = "crowdsec"
BOUNCER_SERVICE = "crowdsec-firewall-bouncer"
BOUNCER_NAME = "firewall-bouncer-host"

def run_cmd(cmd, shell=False):
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing {cmd}: {e.stderr.decode('utf-8')}")
        return None

def check_crowdsec_status():
    print("Checking Crowdsec status...")
    status = run_cmd(["sudo", "systemctl", "is-active", "crowdsec.service"])
    if status != "active":
        print("Crowdsec service is not active. Please ensure it is running.")
        return False
    return True

def check_existing_setup():
    print("Checking for existing configuration...")
    # 1. Check if config file exists and has a non-placeholder key
    if not os.path.exists(BOUNCER_CONFIG):
        return False
    
    current_key = None
    try:
        with open(BOUNCER_CONFIG, 'r') as f:
            for line in f:
                if line.strip().startswith("api_key:"):
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        current_key = parts[1].strip()
    except Exception as e:
        print(f"Error reading config: {e}")
        return False

    if not current_key or len(current_key) < 10: # arbitrary length check
        return False

    # 2. Check if bouncer is registered in Crowdsec
    try:
        # Use json output for reliability
        cmd = ["sudo", "podman", "exec", CONTAINER_NAME, "cscli", "bouncers", "list", "-o", "json"]
        # run_cmd returns stdout string
        output = run_cmd(cmd)
        if output:
            try:
                bouncers = json.loads(output)
                for b in bouncers:
                    if b.get('name') == BOUNCER_NAME and not b.get('revoked'):
                         print(f"Bouncer '{BOUNCER_NAME}' is already registered.")
                         
                         # Optional: Check if service is actually running
                         status = run_cmd(["sudo", "systemctl", "is-active", BOUNCER_SERVICE])
                         if status == "active":
                             print("Bouncer service is active. Setup is idempotent.")
                             return True
                         else:
                             print("Bouncer registered but service not active. Attempting restart...")
                             restart_bouncer()
                             return True
            except json.JSONDecodeError:
                 print("Failed to decode bouncers list JSON.")
    except Exception as e:
        print(f"Error checking bouncer list: {e}")
        
    return False

def generate_key():
    print(f"Generating API key for {BOUNCER_NAME}...")
    # First delete if exists to ensure clean state
    run_cmd(["sudo", "podman", "exec", CONTAINER_NAME, "cscli", "bouncers", "delete", BOUNCER_NAME])
    
    # Create new
    cmd = ["sudo", "podman", "exec", CONTAINER_NAME, "cscli", "bouncers", "add", BOUNCER_NAME, "-o", "json"]
    output = run_cmd(cmd)
    if output:
        try:
            # Check if output is clean JSON or mixed with logs
            # Find the start of JSON structure
            json_start = output.find('{')
            json_end = output.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                 clean_output = output[json_start:json_end]
                 data = json.loads(clean_output)
            else:
                 # Fallback: try raw string if no JSON brackets found (some versions)
                 print(f"DEBUG: No JSON objects found, assuming raw string: {output.strip()}")
                 return output.strip()

            # Depending on version, it might be a list or dict
            if isinstance(data, list):
                return data[0]['api_key']
            if isinstance(data, dict):
                return data['api_key']
            if isinstance(data, str):
                return data
            return data.get('api_key')
        except Exception as e:
            print(f"Failed to parse JSON output: {e}. Output was: {output}")
            return None
    return None

def update_config(api_key):
    print(f"Updating config {BOUNCER_CONFIG}...")
    try:
        # Read existing config
        if not os.path.exists(BOUNCER_CONFIG):
            print("Config file not found. It should have been created by Ansible.")
            return False
            
        with open(BOUNCER_CONFIG, 'r') as f:
            lines = f.readlines()
            
        with open(BOUNCER_CONFIG, 'w') as f:
            for line in lines:
                if line.strip().startswith("api_key:"):
                    f.write(f"api_key: {api_key}\n")
                else:
                    f.write(line)
        print("Config updated successfully.")
        return True
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

def restart_bouncer():
    print("Restarting firewall bouncer...")
    run_cmd(["sudo", "systemctl", "daemon-reload"])
    run_cmd(["sudo", "systemctl", "restart", "crowdsec-firewall-bouncer"])
    print("Bouncer restarted.")

def main():
    if not check_crowdsec_status():
        print("Aborting. Please fix Crowdsec container first (check logs).")
        sys.exit(1)

    if check_existing_setup():
        print("Crowdsec Bouncer is already configured and running.")
        sys.exit(0)
        
    api_key = generate_key()
    if not api_key:
        print("Failed to generate API Key.")
        sys.exit(1)
        
    if update_config(api_key):
        restart_bouncer()
        print("Crowdsec Firewall Bouncer setup complete!")

if __name__ == "__main__":
    main()
