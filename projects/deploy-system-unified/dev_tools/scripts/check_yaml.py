#!/usr/bin/env python3
import yaml
import sys
import os

def check_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            list(yaml.safe_load_all(content))
            return True
    except Exception as e:
        print(f"Error in {filepath}: {e}")
        return False

def main():
    root_dir = os.getcwd()
    error_count = 0
    checked_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip some directories
        if '.git' in dirs:
            dirs.remove('.git')
        if '.ansible' in dirs:
            dirs.remove('.ansible')
        if 'venv' in dirs:
            dirs.remove('venv')
            
        for file in files:
            if file.endswith(('.yml', '.yaml')):
                filepath = os.path.join(root, file)
                checked_count += 1
                if not check_file(filepath):
                    error_count += 1

    print(f"Checked {checked_count} YAML files.")
    if error_count > 0:
        print(f"Found {error_count} YAML errors.")
        sys.exit(1)
    else:
        print("All YAML files valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()