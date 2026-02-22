import importlib.util
import pathlib
import tempfile

# Load the rule module directly (consistent with other ansiblelint rule tests)
rule_path = pathlib.Path(__file__).resolve().parent.parent / 'rules' / 'shim_least_privilege.py'
spec = importlib.util.spec_from_file_location('dsu_rules.shim_least_privilege', str(rule_path))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ShimLeastPrivilegeRule = module.ShimLeastPrivilegeRule


def make_file(path):
    return {'path': path}


def _read_local_init():
    p = pathlib.Path(__file__).resolve().parent.parent / '__init__.py'
    return p.read_text(encoding='utf-8')


def test_shim_rule_passes_on_repository_shim():
    rule = ShimLeastPrivilegeRule()
    file = make_file('ansiblelint/__init__.py')
    matches = rule.matchfile(file)
    assert not matches, f'Expected no matches for compliant shim but got: {matches}'


def test_shim_rule_flags_missing_gating(tmp_path):
    # Create a copy of the real shim but remove gating and logging lines
    original = _read_local_init()
    bad = original
    bad = bad.replace('DSU_ALLOW_ANSIBLELINT_SHIM', 'MISSING_ENV_FLAG')
    bad = bad.replace('_import_originates_from_repo()', 'MISSING_IMPORT_CHECK()')
    bad = bad.replace("DSU-SHIM", 'MISSING_TAG')

    d = tmp_path / 'ansiblelint'
    d.mkdir()
    p = d / '__init__.py'
    p.write_text(bad, encoding='utf-8')

    rule = ShimLeastPrivilegeRule()
    file = make_file(str(p))
    matches = rule.matchfile(file)
    # Expect at least one violation (gating + logging missing)
    assert any('gated' in str(m) or 'audit log' in str(m) for m in matches), matches


def test_shim_rule_flags_network_calls(tmp_path):
    # Create a shim-like file that contains a network call
    original = _read_local_init()
    bad = original + "\nimport requests\n# simulate risky call removed at runtime\n"

    d = tmp_path / 'ansiblelint'
    d.mkdir()
    p = d / '__init__.py'
    p.write_text(bad, encoding='utf-8')

    rule = ShimLeastPrivilegeRule()
    file = make_file(str(p))
    matches = rule.matchfile(file)
    assert any('network' in str(m) or 'subprocess' in str(m) for m in matches), matches
