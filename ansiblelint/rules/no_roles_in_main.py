from ansiblelint.rules import AnsibleLintRule


class NoRolesInMainRule(AnsibleLintRule):
    id = 'DSU001'
    shortdesc = 'Do not use top-level roles in main.yml'
    description = 'main.yml must remain a pristine base; use branch_templates/*.yml for role lists and name your playbook site.yml.'
    severity = 'HIGH'
    tags = ['roles', 'best-practice']
    version_added = '1.0.0'
    version_changed = '1.0.1'

    def _get_path(self, file):
        if hasattr(file, 'path'):
            return str(file.path)
        if hasattr(file, 'get'):
            return file.get('path', '')
        return str(file)

    def matchplay(self, file, play):
        # Be defensive: only operate on dict plays and ensure roles is a non-empty list
        filename = self._get_path(file)
        # Normalize path checking for both absolute and relative paths
        norm_path = filename.replace('\\', '/')
        
        # Target any 'main.yml' that is not a task/handler/meta/defaults/vars file
        if not norm_path.endswith('main.yml'):
            return False
            
        # Avoid identifying files inside standard role structure as violations
        path_parts = norm_path.split('/')
        reserved_dirs = {'tasks', 'handlers', 'defaults', 'vars', 'meta', 'roles'}
        # Check if any parent directory is a reserved name
        if any(part in reserved_dirs for part in path_parts[:-1]):
            return False
            
        if not isinstance(play, dict):
            return False
        roles = play.get('roles')
        if isinstance(roles, list) and len(roles) > 0:
            return True
        return False

    def matchyaml(self, file):
        # YAML-aware check: process documents safely and return a list of messages
        matches = []
        filename = self._get_path(file)
        norm_path = filename.replace('\\', '/')
        
        if not norm_path.endswith('main.yml'):
            return matches
            
        # Avoid identifying files inside standard role structure as violations
        path_parts = norm_path.split('/')
        reserved_dirs = {'tasks', 'handlers', 'defaults', 'vars', 'meta', 'roles'}
        if any(part in reserved_dirs for part in path_parts[:-1]):
            return matches

        # Handle modern Lintable object or legacy dict
        yaml_data = getattr(file, 'data', None)
        if yaml_data is None and hasattr(file, 'get'):
             # Fallback for older versions if they don't pass data but file is dict? 
             # Actually matchyaml(self, file) implies we must get data from file.
             pass
        
        if yaml_data is None:
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
