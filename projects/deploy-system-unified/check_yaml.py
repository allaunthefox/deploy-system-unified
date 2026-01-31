#!/usr/bin/env python3
import yaml
import sys

try:
    with open('roles/core/vps_optimization/tasks/providers/contabo.yml', 'rb') as f:
        content = f.read()
        print("File content:", repr(content.decode('utf-8')))
        data = yaml.safe_load(content)
        print("YAML is valid")
        print("Data:", data)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    print(traceback.format_exc())