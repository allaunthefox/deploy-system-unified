# =============================================================================
# Audit Event Identifier: DSU-PYS-500103
# Last Updated: 2026-02-28
# =============================================================================
import re
from pathlib import Path
from ansiblelint.errors import MatchError
from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule


class ShimLeastPrivilegeRule(AnsibleLintRule):
    id = 'DSU004'
    shortdesc = 'Test-only shims must follow least-privilege and audit rules'
    description = (
        'Detects ansiblelint/other in-repo "shim" modules and enforces:\n'
        '- explicit gating (env override / repo-origin / pytest / CI)\n'
        "- shim marker(s) set (e.g. __dsu_shim__ = True)\n"
        '- structured audit log (tagged `DSU-SHIM`)\n'
        '- no network/subprocess/filesystem side-effects at import time\n'
        '- limited, explicit exports (no wildcard/unsafes)\n'
    )
    severity = 'MEDIUM'
    tags = ['security', 'audit', 'shims']
    version_added = '1.0.3'

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

    def matchfile(self, file):
        """Inspect `ansiblelint/__init__.py` for shim safety and least-privilege.

        Returns a list of MatchError or strings describing problems.
        """
        matches = []
        filename = self._get_path(file)
        norm_path = filename.replace('\\', '/')

        # Only operate on the repository's shim entrypoint
        if not norm_path.endswith('ansiblelint/__init__.py'):
            return matches

        # Resolve file path relative to repo if necessary
        file_path = Path(filename)
        if not file_path.is_file():
            # Try repo-relative
            repo_root = Path(__file__).resolve().parents[1]
            candidate = repo_root / filename
            if candidate.exists():
                file_path = candidate
            else:
                return matches

        try:
            text = file_path.read_text(encoding='utf-8')
        except Exception:
            return matches

        # 1) Gating check (env OR repo-origin OR pytest/CI)
        gating_ok = bool(
            re.search(r'DSU_ALLOW_ANSIBLELINT_SHIM', text)
            or re.search(r'_import_originates_from_repo', text)
            or re.search(r'pytest|PYTEST_CURRENT_TEST', text)
            or re.search(r'\bCI\b', text)
        )
        if not gating_ok:
            matches.append(self._make_match(file, 'Shim activation must be explicitly gated (env/repo/pytest/CI) — enforces least privilege'))

        # 2) Shim markers must be present on fallback modules
        if not re.search(r"__dsu_shim__\s*=\s*True", text):
            matches.append(self._make_match(file, 'Shim-created modules must set __dsu_shim__ = True (audit marker)'))

        # 3) Must emit an auditable DSU-SHIM log entry with logger 'dsu.ansiblelint_shim'
        if not (re.search(r"dsu\.ansiblelint_shim", text) and re.search(r"DSU-SHIM", text)):
            matches.append(self._make_match(file, "Shim must emit a structured audit log with tag 'DSU-SHIM' via logger 'dsu.ansiblelint_shim'"))

        # 4) Prohibit risky imports / runtime side-effects at import time
        risky_patterns = [r'\brequests\b', r'\bsocket\b', r'\bsubprocess\b', r'\bos\.system\b', r'\bPopen\b', r'\burllib\b']
        for pat in risky_patterns:
            if re.search(pat, text):
                matches.append(self._make_match(file, 'Shim must not perform network/subprocess operations at import time (principle of least privilege)'))
                break

        # 5) Avoid opening/writing files at import time
        if re.search(r"open\(.*['\"]w['\"]", text):
            matches.append(self._make_match(file, 'Shim must not write files at import time'))

        # 6) Ensure __all__ is explicit and does not expose internal markers
        all_match = re.search(r"__all__\s*=\s*\[([^\]]*)\]", text, re.S)
        if all_match:
            items = all_match.group(1)
            if '*' in items or '__dsu_shim__' in items:
                matches.append(self._make_match(file, '__all__ must list explicit, safe exports and must not expose internal shim markers'))
        else:
            matches.append(self._make_match(file, '__all__ missing — exports should be explicitly enumerated for auditability'))

        return matches
