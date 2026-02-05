from ansiblelint.rules.no_gpu_capabilities import NoGpuCapabilitiesRule


def make_file(path):
    return {'path': path}


def test_rejects_non_capabilities():
    rule = NoGpuCapabilitiesRule()
    file = make_file('branch_templates/gpu_workstations.yml')
    yaml_doc = {
        'vars': {
            'quadlet_gpu_capabilities': ['gpu', 'compute'],
            'capabilities': ['CAP_NET_BIND_SERVICE', 'gpu'],
        }
    }
    matches = rule.matchyaml(file, yaml_doc)
    assert matches, "Expected non-CAP_* values to be flagged"


def test_allows_cap_only():
    rule = NoGpuCapabilitiesRule()
    file = make_file('branch_templates/production_servers.yml')
    yaml_doc = {'vars': {'quadlet_gpu_capabilities': ['CAP_NET_BIND_SERVICE']}}
    matches = rule.matchyaml(file, yaml_doc)
    assert not matches, "Expected CAP_* values to pass"
