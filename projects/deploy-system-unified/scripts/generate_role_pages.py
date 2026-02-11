import os
import yaml
import re

ROLES_DIR = "projects/deploy-system-unified/roles"
WIKI_ROLES_DIR = "wiki_pages/roles"

def get_role_info(role_path):
    role_name = os.path.relpath(role_path, ROLES_DIR)
    wiki_filename = role_name.replace("/", "_") + ".md"
    
    tasks_file = os.path.join(role_path, "tasks", "main.yml")
    defaults_file = os.path.join(role_path, "defaults", "main.yml")
    
    description = ""
    tasks = []
    variables = []
    
    if os.path.exists(tasks_file):
        with open(tasks_file, 'r') as f:
            content = f.read()
            # Try to get top-level comment as description
            match = re.search(r'^---\n#\s*(.*)', content)
            if match:
                description = match.group(1)
            
            try:
                data = yaml.safe_load(content)
                if isinstance(data, list):
                    for task in data:
                        if isinstance(task, dict) and 'name' in task:
                            tasks.append(task['name'])
            except:
                pass

    if os.path.exists(defaults_file):
        with open(defaults_file, 'r') as f:
            try:
                data = yaml.safe_load(f)
                if isinstance(data, dict):
                    variables = list(data.keys())
            except:
                pass
                
    return {
        "role_name": role_name,
        "wiki_filename": wiki_filename,
        "description": description,
        "tasks": tasks,
        "variables": variables
    }

def generate_wiki_page(info):
    content = f"# {info['role_name']}\n\n"
    content += f"**Role Path**: `roles/{info['role_name']}`\n\n"
    
    if info['description']:
        content += f"## Description\n{info['description']}\n\n"
    else:
        content += "## Description\n*No description provided.*\n\n"
        
    if info['tasks']:
        content += "## Key Tasks\n"
        for task in info['tasks']:
            content += f"- {task}\n"
        content += "\n"
        
    if info['variables']:
        content += "## Default Variables\n"
        for var in info['variables']:
            content += f"- `{var}`\n"
        content += "\n"
        
    content += "---\n*This page was automatically generated from role source code.*"
    return content

def main():
    if not os.path.exists(WIKI_ROLES_DIR):
        os.makedirs(WIKI_ROLES_DIR)
        
    for root, dirs, files in os.walk(ROLES_DIR):
        # We only want depth 2 (e.g., core/bootstrap)
        rel_path = os.path.relpath(root, ROLES_DIR)
        parts = rel_path.split(os.sep)
        
        if len(parts) == 2:
            info = get_role_info(root)
            wiki_content = generate_wiki_page(info)
            wiki_path = os.path.join(WIKI_ROLES_DIR, info['wiki_filename'])
            
            with open(wiki_path, 'w') as f:
                f.write(wiki_content)
            print(f"Generated {wiki_path}")

if __name__ == "__main__":
    main()
