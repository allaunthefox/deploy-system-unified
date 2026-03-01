# =============================================================================
# Audit Event Identifier: DSU-PYS-500106
# Last Updated: 2026-02-28
# =============================================================================

# Import the rule class directly
# Import the rule module directly from file to ensure tests load the local rule
import importlib.util
import pathlib

rule_path = pathlib.Path(__file__).resolve().parent.parent / 'rules' / 'no_roles_in_main.py'
spec = importlib.util.spec_from_file_location('dsu_rules.no_roles_in_main', str(rule_path))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
NoRolesInMainRule = module.NoRolesInMainRule


def make_file(path):
    return {'path': path}


def test_matchyaml_detects_roles_in_main():
    rule = NoRolesInMainRule()
    file = make_file('projects/deploy-system-unified/main.yml')
    yaml_doc = [{'name': 'test', 'hosts': 'all', 'roles': ['core/bootstrap']}]
    matches = rule.matchyaml(file, yaml_doc)
    assert matches, "Expected matches when top-level roles exist in main.yml"


def test_matchyaml_passes_when_no_roles():
    rule = NoRolesInMainRule()
    file = make_file('projects/deploy-system-unified/main.yml')
    yaml_doc = [{'name': 'test', 'hosts': 'all'}]
    matches = rule.matchyaml(file, yaml_doc)
    assert not matches, "Expected no matches when no top-level roles are present"


def test_rule_ignores_branch_templates():
    rule = NoRolesInMainRule()
    file = make_file('projects/deploy-system-unified/branch_templates/production_servers.yml')
    yaml_doc = [{'name': 'test', 'hosts': 'all', 'roles': ['core/bootstrap']}]
    matches = rule.matchyaml(file, yaml_doc)
    assert not matches, "Expected rule to ignore branch templates"
