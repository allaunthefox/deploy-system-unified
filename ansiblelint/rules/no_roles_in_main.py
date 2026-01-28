from ansiblelint.rules import AnsibleLintRule


class NoRolesInMainRule(AnsibleLintRule):
    id = 'DSU001'
    shortdesc = 'Do not use top-level roles in projects/deploy-system-unified/main.yml'
    description = 'main.yml must remain a pristine base; use branch_templates/*.yml for role lists.'
    severity = 'HIGH'
    tags = ['roles', 'best-practice']
    version_added = '1.0.0'

    def matchplay(self, file, play):
        filename = file.get('path', '')
        # Normalize path checking for both absolute and relative paths
        if filename.replace('\\\\', '/').endswith('projects/deploy-system-unified/main.yml'):
            return isinstance(play, dict) and 'roles' in play and bool(play.get('roles'))
        return False
