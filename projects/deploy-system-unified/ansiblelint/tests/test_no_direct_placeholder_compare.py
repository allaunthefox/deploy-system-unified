from ansiblelint.rules.no_direct_placeholder_compare import NoDirectPlaceholderCompareRule


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
