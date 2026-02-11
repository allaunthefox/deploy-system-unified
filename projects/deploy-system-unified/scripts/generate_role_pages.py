#!/usr/bin/env python3
"""Script to generate role pages from role source code."""

import os
import yaml
import re


ROLES_DIR = "projects/deploy-system-unified/roles"
WIKI_ROLES_DIR = "wiki_pages/roles"
ROLE_REFERENCE_FILE = "wiki_pages/Role_Reference.md"


def get_manual_descriptions():
    """Get manual descriptions from Role_Reference.md."""
    descriptions = {}
    if not os.path.exists(ROLE_REFERENCE_FILE):
        return descriptions

    with open(ROLE_REFERENCE_FILE, 'r') as f:
        content = f.read()

    # Pattern to match role headers and their descriptions
    # ### `category/role` — [Read details](...)
    # **Summary Title**
    # Detailed description...
    sections = re.split(r'### `([^`]+)`', content)

    for i in range(1, len(sections), 2):
        role_name = sections[i]
        text = sections[i+1]

        # Extract everything after the [Read details] line until the next header or end of file
        # We want to skip the "Read details" link and the bold summary title if possible, or just take it all.
        match = re.search(r'\[Read details\].*?\n(.*)', text, re.DOTALL)
        if match:
            desc = match.group(1).strip()
            # Stop at the next role or section
            desc = re.split(r'\n##', desc)[0].strip()
            descriptions[role_name] = desc

    return descriptions


def get_role_info(role_path, manual_descriptions):
    """Get information about a role from its source code."""
    role_name = os.path.relpath(role_path, ROLES_DIR)
    wiki_filename = role_name.replace("/", "_") + ".md"

    tasks_file = os.path.join(role_path, "tasks", "main.yml")
    defaults_file = os.path.join(role_path, "defaults", "main.yml")

    description = manual_descriptions.get(role_name, "")
    tasks = []
    variables = []

    # If no manual description, try to get top-level comment as fallback
    if not description and os.path.exists(tasks_file):
        with open(tasks_file, 'r') as f:
            content = f.read()
            match = re.search(r'^---\n#\s*(.*)', content)
            if match:
                description = match.group(1)

    if os.path.exists(tasks_file):
        with open(tasks_file, 'r') as f:
            try:
                # We need to handle potential includes
                content = f.read()
                data = yaml.safe_load(content)
                if isinstance(data, list):
                    for task in data:
                        if isinstance(task, dict):
                            if 'name' in task:
                                tasks.append(task['name'])
                            elif 'include_tasks' in task:
                                tasks.append(f"Include: {task['include_tasks']}")
                            elif 'import_tasks' in task:
                                tasks.append(f"Import: {task['import_tasks']}")
            except Exception:
                pass

    if os.path.exists(defaults_file):
        with open(defaults_file, 'r') as f:
            try:
                data = yaml.safe_load(f)
                if isinstance(data, dict):
                    variables = list(data.keys())
            except Exception:
                pass

    return {
        "role_name": role_name,
        "wiki_filename": wiki_filename,
        "description": description,
        "tasks": tasks,
        "variables": variables
    }


def generate_wiki_page(info):
    """Generate wiki page content for a role."""
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
    """Main function to generate wiki pages for all roles."""
    if not os.path.exists(WIKI_ROLES_DIR):
        os.makedirs(WIKI_ROLES_DIR)

    manual_descriptions = get_manual_descriptions()

    for root, dirs, files in os.walk(ROLES_DIR):
        rel_path = os.path.relpath(root, ROLES_DIR)
        parts = rel_path.split(os.sep)

        if len(parts) == 2:
            info = get_role_info(root, manual_descriptions)
            wiki_content = generate_wiki_page(info)
            wiki_path = os.path.join(WIKI_ROLES_DIR, info['wiki_filename'])

            with open(wiki_path, 'w') as f:
                f.write(wiki_content)
            print(f"Generated {wiki_path}")


if __name__ == "__main__":
    main()