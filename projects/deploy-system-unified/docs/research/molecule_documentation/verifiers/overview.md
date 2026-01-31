# Molecule Verifiers
## Overview
Molecule verifiers are used to validate that your Ansible roles have correctly configured the test instances. They run after the converge step to verify the system state.

## Supported Verifiers
### TestInfra
The default verifier using Python test framework:
```yaml
verifier:
  name: testinfra
  directory: ../tests/
  options:
    verbose: true
  env:
    PYTHONPATH: ../test/
  additional_files_or_dirs:
    - ../test/
```

Example test file (`tests/test_default.py`):
```python
def test_pkg_installed(host):
    pkg = host.package('nginx')
    assert pkg.is_installed
def test_svc_running(host):
    svc = host.service('nginx')
    assert svc.is_running
    assert svc.is_enabled

def test_port_listening(host):
    sock = host.socket("tcp://0.0.0.0:80")
    assert sock.is_listening
```
### Goss
Lightweight and fast verification tool using YAML:
```yaml
verifier:
  name: goss
  directory: ../test/integration/${MOLECULE_SCENARIO_NAME}/
  playbook: ../resources/playbooks/verify-goss.yml
```

Example Goss file (`test/integration/default/goss.yaml`):
```yaml
package:
  nginx:
    installed: true
service:
  nginx:
    enabled: true
    running: true

port:
  tcp:80:
    listening: true
process:
  nginx:
    running: true

user:
  nginx:
    exists: true
```
### InSpec
Infrastructure testing framework by Chef:
```yaml
verifier:
  name: inspec
  directory: ../test/integration/${MOLECULE_SCENARIO_NAME}/
```

Example InSpec control (`test/integration/default/controls/sample.rb`):
```ruby
describe package('nginx') do
  it { should be_installed }
end
describe service('nginx') do
  it { should be_installed }
  it { should be_enabled }
  it { should be_running }
end

describe port(80) do
  it { should be_listening }
end
```
### Serverspec
Ruby-based testing framework:
```yaml
verifier:
  name: serverspec
  directory: ../test/integration/${MOLECULE_SCENARIO_NAME}/
```

## Verifier Configuration
### TestInfra Options
- `options`: Command-line options for pytest
- `env`: Environment variables
- `directory`: Test directory location
- `additional_files_or_dirs`: Additional test files

### Goss Options
- `directory`: Goss file directory
- `playbook`: Custom playbook for Goss
- `test_binary`: Path to goss binary
- `goss_config`: Path to goss configuration
### InSpec Options
- `directory`: InSpec test directory
- `options`: Command-line options for inspec
- `env`: Environment variables
- `sudo`: Whether to run with sudo

## Verification Strategies
### Functional Testing
Verify that services are running and responding:
- Check service status
- Verify ports are listening
- Test application functionality
- Validate configurations

### Security Testing
Verify security configurations:
- Check file permissions
- Validate user accounts
- Verify security settings
- Test access controls
### Compliance Testing
Verify compliance with standards:
- Check configuration files
- Validate installed packages
- Verify system settings
- Test security policies

## Best Practices
### Test Structure
- Organize tests by functionality
- Use descriptive test names
- Test both positive and negative cases
- Keep tests focused and atomic
- Document test purposes

### Assertion Quality
- Use specific assertions
- Test expected outcomes
- Verify state changes
- Check error conditions
### Test Maintenance
- Keep tests up-to-date with role changes
- Run tests regularly
- Monitor test performance
- Refactor as needed
- Document test expectations

## Choosing a Verifier
Select a verifier based on:
- **Language Familiarity**: Python (TestInfra), YAML (Goss), Ruby (InSpec)
- **Performance**: Goss is typically fastest
- **Features**: Available assertion types
- **Community**: Support and documentation
- **Integration**: With existing tools
