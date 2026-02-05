# Ansible Modules

Modules are the executable bits of Ansible that do the actual work. Each module is a self-contained script that can be invoked by the Ansible API, or by the `ansible` or `ansible-playbook` programs.

## Categories of Modules

### Core Modules
These are maintained by the Ansible core team and are guaranteed to work in the same way in each new Ansible release.

### Community Modules
These are maintained by the community and may have different release cycles.

## Common Module Patterns

### Action Plugins
Action plugins wrap the execution of modules, and are executed on the controller before the module is sent to the remote host.

### Connection Plugins
Connection plugins define how to communicate with the target host.

### Lookup Plugins
Lookup plugins allow access to data in Ansible from outside sources.

### Filter Plugins
Filter plugins transform data from one format to another.

## Important Modules

### Core Modules

#### File Modules
- `copy`: Copy files to remote locations
- `file`: Set attributes of files
- `template`: Template a file out to a remote server
- `lineinfile`: Manage lines in text files
- `blockinfile`: Insert/update/remove a text block surrounded by marker lines
- `assemble`: Assemble configuration files from fragments
- `find`: Return a list of files based on specific criteria
- `stat`: Retrieve file or file system status

#### System Modules
- `user`: Manage user accounts
- `group`: Manage group accounts
- `service`: Manage services
- `systemd`: Manage systemd units
- `cron`: Manage crontab entries
- `authorized_key`: Add or remove authorized keys for particular user accounts

#### Commands Modules
- `command`: Execute commands
- `shell`: Execute shell commands
- `raw`: Execute a low-down and dirty command
- `script`: Runs a local script on a remote node after transferring it

#### Packaging Modules
- `package`: Generic packaging module
- `yum`: Manages packages with the yum package manager
- `apt`: Manages packages with the APT package manager
- `dnf`: Manages packages with the DNF package manager
- `pip`: Manages Python library dependencies
- `gem`: Manages Ruby gems

#### Net Tools Modules
- `get_url`: Downloads files from HTTP, HTTPS, or FTP to node
- `uri`: Interacts with webservices
- `wait_for`: Waits for a condition before continuing
- `wait_for_connection`: Waits for remote connection to become available

#### Utilities Modules
- `debug`: Print statements during execution
- `assert`: Asserts given expressions are true
- `fail`: Fail with custom message
- `pause`: Pause playbook execution
- `meta`: Execute Ansible 'actions'

## Module Parameters

### Common Parameters
Most Ansible modules accept these common parameters:

- `become`: Run operations with become (nopasswd implied)
- `become_method`: Privilege escalation method
- `become_user`: User to become
- `check_mode`: Don't make any changes; instead, try to predict some of the changes that may occur
- `diff`: When changing (small) files and templates, show the differences in those files
- `environment`: Additional environment variables to set for the task
- `no_log`: Disable logging for this task
- `register`: Variable name to save the output of the module
- `until`: Conditional string for task retries
- `retries`: Number of retries before giving up
- `delay`: Number of seconds to wait between retries

## Module Return Values

Modules return data in JSON format that can be accessed using the `register` keyword.

```yaml
- name: Get system information
  setup:
  register: system_info

- name: Display system information
  debug:
    var: system_info
```

## Module Documentation

Module documentation can be accessed using the `ansible-doc` command:

```bash
ansible-doc module_name
ansible-doc -l  # List all available modules
```

## Developing Custom Modules

Custom modules can be developed in any language that can return JSON. Python is the most common choice due to helper libraries provided by Ansible.

Basic structure of a Python module:
```python
#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, type='str'),
            state=dict(default='present', choices=['present', 'absent'])
        )
    )

    # Module logic here
    module.exit_json(changed=True, msg="Success")

if __name__ == '__main__':
    main()
```