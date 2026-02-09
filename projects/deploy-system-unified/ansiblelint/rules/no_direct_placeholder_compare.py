import re
from ansiblelint.errors import MatchError
from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule


class NoDirectPlaceholderCompareRule(AnsibleLintRule):
    id = 'DSU003'
    shortdesc = 'Avoid direct comparisons to placeholder default values'
    description = (
        'Directly comparing variables to placeholder values (e.g., CHANGE_ME, '
        'CHANGE_ME_IN_*) is brittle and may produce fatal errors in CI. Use a '
        'defensive pattern: check variable is defined, use a safe default, and '
        'ensure non-empty length.'
    )
    severity = 'MEDIUM'
    tags = ['secrets', 'validation']
    version_added = '1.0.2'

    def _get_path(self, file):
        if hasattr(file, 'path'):
            return str(file.path)
        if hasattr(file, 'get'):
            return file.get('path', '')
        return str(file)

    def _make_match(self, file, message):
        if isinstance(file, Lintable):
            return MatchError(lintable=file, rule=self, message=message)
        return message

    def _iter_nodes(self, obj):
        # Recursively yield all scalar nodes in YAML structures
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield from self._iter_nodes(k)
                yield from self._iter_nodes(v)
        elif isinstance(obj, list):
            for item in obj:
                yield from self._iter_nodes(item)
        else:
            yield obj

    def _collect_bad_values(self, obj, out):
        """Recursively collect literals from any 'bad_values' lists in the doc.

        Args:
            obj: YAML node (dict/list/scalar)
            out: set to populate with bad values found (strings)
        """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == 'bad_values' and isinstance(v, list):
                    for i in v:
                        if isinstance(i, str):
                            out.add(i)
                else:
                    self._collect_bad_values(v, out)
        elif isinstance(obj, list):
            for item in obj:
                self._collect_bad_values(item, out)
        # scalars ignored

    def matchyaml(self, file, yaml_doc=None):
        matches = []
        filename = self._get_path(file)
        norm_path = filename.replace('\\', '/')

        # Skip test fixtures and intentional placeholder files
        skip_fragments = ['/molecule/', '/defaults/', '/templates/', '/docs/', '/inventory/']
        if any(fragment in norm_path for fragment in skip_fragments):
            return matches

        yaml_data = yaml_doc
        if yaml_data is None:
            yaml_data = getattr(file, 'data', None)
        if yaml_data is None and hasattr(file, 'get'):
            yaml_data = file.get('data')
        if yaml_data is None:
            return matches

        # Precompile regexes for performance
        placeholder_re = re.compile(r'CHANGE_ME')
        operator_re = re.compile(r"!=|==|\bin\b|\bnot\s+in\b")
        default_re = re.compile(r"\|\s*default\s*\(\s*['\"]CHANGE_ME")

        docs = yaml_data if isinstance(yaml_data, list) else [yaml_data]
        for doc in docs:
            try:
                # Collect any 'bad_values' entries that indicate intentional placeholder guards
                bad_values = set()
                self._collect_bad_values(doc, bad_values)

                for node in self._iter_nodes(doc):
                    if not isinstance(node, str):
                        continue
                    s = node
                    # Detect direct comparisons and default comparisons to placeholders
                    if placeholder_re.search(s) and (
                        operator_re.search(s) or default_re.search(s)
                    ):
                        # If the placeholder in question is covered by a nearby 'bad_values' list, ignore it
                        if any(bv and bv in s for bv in bad_values):
                            continue
                        matches.append(self._make_match(file, f"Direct placeholder comparison detected: {s}"))
            except Exception:
                # Be tolerant of unexpected structures
                continue
        return matches
