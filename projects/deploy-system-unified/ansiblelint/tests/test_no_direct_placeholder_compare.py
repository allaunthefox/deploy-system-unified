# Import the rule module directly from file to avoid import collision with installed 'ansiblelint' package
import importlib.util
import pathlib

rule_path = pathlib.Path(__file__).resolve().parent.parent / 'rules' / 'no_direct_placeholder_compare.py'
spec = importlib.util.spec_from_file_location('dsu_rules.no_direct_placeholder_compare', str(rule_path))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
NoDirectPlaceholderCompareRule = module.NoDirectPlaceholderCompareRule


def make_file(path):
    return {'path': path}


def test_flags_direct_comparison():
    rule = NoDirectPlaceholderCompareRule()
    file = make_file('roles/example/tasks/main.yml')
    yaml_doc = {
        'tasks': [
            {
                'name': 'bad comparison',
                'ansible.builtin.assert': {'that': ['foo != "CHANGE_ME"']},
            }
        ]
    }
    matches = rule.matchyaml(file, yaml_doc)
    assert matches, "Expected direct placeholder comparison to be flagged"


def test_flags_default_comparison():
    rule = NoDirectPlaceholderCompareRule()
    file = make_file('roles/example/tasks/main.yml')
    yaml_doc = {
        'tasks': [
            {
                'name': 'bad default comparison',
                'ansible.builtin.assert': {
                    'that': ["foo | default('CHANGE_ME') != 'CHANGE_ME'"]
                },
            }
        ]
    }
    matches = rule.matchyaml(file, yaml_doc)
    assert matches, "Expected default->placeholder comparison to be flagged"


def test_flags_equality_comparison():
    rule = NoDirectPlaceholderCompareRule()
    file = make_file('roles/example/tasks/main.yml')
    yaml_doc = {
        'tasks': [
            {
                'name': 'equality comparison',
                'ansible.builtin.assert': {'that': ["foo == 'CHANGE_ME'"]},
            }
        ]
    }
    matches = rule.matchyaml(file, yaml_doc)
    assert matches, "Expected equality comparison to be flagged"


def test_flags_in_membership():
    rule = NoDirectPlaceholderCompareRule()
    file = make_file('roles/example/tasks/main.yml')
    yaml_doc = {
        'tasks': [
            {
                'name': 'in membership',
                'ansible.builtin.assert': {'that': ["'CHANGE_ME' in foo"]},
            }
        ]
    }
    matches = rule.matchyaml(file, yaml_doc)
    assert matches, "Expected membership comparison to be flagged"


def test_flags_default_equality():
    rule = NoDirectPlaceholderCompareRule()
    file = make_file('roles/example/tasks/main.yml')
    yaml_doc = {
        'tasks': [
            {
                'name': 'default equality',
                'ansible.builtin.assert': {
                    'that': ["foo | default('CHANGE_ME') == 'CHANGE_ME'"]
                },
            }
        ]
    }
    matches = rule.matchyaml(file, yaml_doc)
    assert matches, "Expected default equality comparison to be flagged"


def test_ignores_molecule_and_defaults():
    rule = NoDirectPlaceholderCompareRule()
    file = make_file('roles/example/molecule/negative/converge.yml')
    yaml_doc = {
        'tasks': [
            {
                'name': 'allowed in molecule fixtures',
                'ansible.builtin.assert': {'that': ['foo != "CHANGE_ME"']},
            }
        ]
    }
    matches = rule.matchyaml(file, yaml_doc)
    assert not matches, "Expected the rule to ignore molecule fixtures"
