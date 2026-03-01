# =============================================================================
# Audit Event Identifier: DSU-PYS-500101
# Last Updated: 2026-02-28
# =============================================================================
from ansiblelint.errors import MatchError
from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule


class NoGpuCapabilitiesRule(AnsibleLintRule):
    id = 'DSU002'
    shortdesc = 'Disallow non-CAP_* entries in capabilities lists'
    description = (
        'Capability lists must contain only Linux CAP_* values. Strings like '
        '"gpu", "compute", "video", or "display" are not kernel capabilities.'
    )
    severity = 'HIGH'
    tags = ['capabilities', 'security', 'best-practice']
    version_added = '1.0.0'
    version_changed = '1.0.1'

    def _get_path(self, file):
        if hasattr(file, 'path'):
            return str(file.path)
        if hasattr(file, 'get'):
            return file.get('path', '')
        return str(file)

    def _invalid_caps(self, value):
        if not isinstance(value, list):
            return []
        invalid = []
        for item in value:
            if isinstance(item, str) and not item.startswith('CAP_'):
                invalid.append(item)
        return invalid

    def _make_match(self, file, message):
        if isinstance(file, Lintable):
            return MatchError(lintable=file, rule=self, message=message)
        return message

    def matchyaml(self, file, yaml_doc=None):
        matches = []
        yaml_data = yaml_doc
        if yaml_data is None:
            yaml_data = getattr(file, 'data', None)
        if yaml_data is None and isinstance(file, dict):
            yaml_data = file.get('data')
        if yaml_data is None:
            return matches

        docs = yaml_data if isinstance(yaml_data, list) else [yaml_data]
        for doc in docs:
            if not isinstance(doc, dict):
                continue
            # Walk the doc recursively for keys that represent capabilities lists.
            stack = [doc]
            while stack:
                node = stack.pop()
                if isinstance(node, dict):
                    for key, value in node.items():
                        if key in ('capabilities', 'quadlet_gpu_capabilities'):
                            invalid = self._invalid_caps(value)
                            if invalid:
                                matches.append(
                                    self._make_match(
                                        file,
                                        f"Invalid capabilities in '{key}': {', '.join(invalid)}",
                                    )
                                )
                        else:
                            if isinstance(value, (dict, list)):
                                stack.append(value)
                elif isinstance(node, list):
                    for item in node:
                        if isinstance(item, (dict, list)):
                            stack.append(item)
        return matches