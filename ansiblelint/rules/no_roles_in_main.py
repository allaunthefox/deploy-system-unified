from ansiblelint.rules import AnsibleLintRule


class NoRolesInMainRule(AnsibleLintRule):
    id = 'DSU001'
    shortdesc = 'Do not use top-level roles in projects/deploy-system-unified/main.yml'
    description = 'main.yml must remain a pristine base; use branch_templates/*.yml for role lists.'
    severity = 'HIGH'
    tags = ['roles', 'best-practice']
    version_added = '1.0.0'
    version_changed = '1.0.0'

    def matchplay(self, file, play):
        # Be defensive: only operate on dict plays and ensure roles is a non-empty list
        filename = file.get('path', '')
        # Normalize path checking for both absolute and relative paths
        if not filename.replace('\\\\', '/').endswith('projects/deploy-system-unified/main.yml'):
            return False
        if not isinstance(play, dict):
            return False
        roles = play.get('roles')
        if isinstance(roles, list) and len(roles) > 0:
            return True
        return False

    def matchyaml(self, file, yaml_data):
        # YAML-aware check: process documents safely and return a list of messages
        matches = []
        filename = file.get('path', '')
        if not filename.replace('\\\\', '/').endswith('projects/deploy-system-unified/main.yml'):
            return matches
        docs = yaml_data if isinstance(yaml_data, list) else [yaml_data]
        for idx, play in enumerate(docs):
            try:
                if isinstance(play, dict):
                    roles = play.get('roles')
                    if isinstance(roles, list) and roles:
                        matches.append(f"Top-level 'roles' found in play index {idx}")
            except Exception:
                # Be tolerant of unexpected structures
                continue
        return matches
