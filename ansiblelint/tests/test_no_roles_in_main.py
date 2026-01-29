import yaml
from ansiblelint.rules import AnsibleLintRule
from ansiblelint.rules import RulesCollection
from ansiblelint.rules import RulesCollection
from ansiblelint.rules import RulesCollection
from ansiblelint.rules import RulesCollection

# Import the rule class directly
from ansiblelint.rules.no_roles_in_main import NoRolesInMainRule


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
