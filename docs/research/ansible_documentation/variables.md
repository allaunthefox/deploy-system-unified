# variables

Variables in Ansible allow you to abstract your playbooks and make them reusable. They can store values that can be used throughout your playbooks and roles.

## Variable Precedence

Ansible has a specific order of precedence for variables. From highest to lowest:

1. `command_line_values` (e.g. `-e` arguments to ansible-playbook)
2. `role_defaults` (lowest priority)
3. `group_vars` (by group)
4. `host_vars` (by host)
5. `facts` / `magic_variables`
6. `vars` (by block/task)
7. `vars_files`
8. `vars_prompt`
9. `role_vars` (by role)
10. `set_facts` / `registered_vars`
11. `play_vars_prompt`
12. `play_vars_files`
13. `play_vars`
14. `role_params` (parameters passed to roles)
15. `include_params` (parameters passed to includes)
16. `block_vars` (only for tasks in block)
17. `task_vars` (only for the task)
18. `extra_vars` (e.g. `-e` arguments to ansible-playbook) (highest priority)

## Variable Names

Variable names should:

- Contain letters, numbers, underscores, and hyphens
- Start with a letter
- Be lowercase when possible
- Use underscores instead of camelCase
- Be descriptive and meaningful

## Defining Variables

### In Playbook

```yaml
- hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
  tasks:
    - name: Ensure apache is installed
      package:
        name: apache2
        state: present
```

### In Variable Files

```yaml
# vars.yml
---
http_port: 80
max_clients: 200
```

```yaml
# In playbook
- hosts: webservers
  vars_files:
    - vars.yml
  tasks:
    - name: Ensure apache is installed
      package:
        name: apache2
        state: present
```

### In Inventory

```ini
# inventory
[webservers]
web1.example.com http_port=8080
web2.example.com http_port=80
```

### At Runtime

```bash
ansible-playbook SITE.YML -e "http_port=8080"
```

## Variable Types

### Scalars

```yaml
---
var_string: "hello world"
var_number: 42
var_boolean: true
```

### Lists

```yaml
---
var_list:
  - item1
  - item2
  - item3

# Or
var_list: [item1, item2, item3]
```

### Dictionaries

```yaml
---
var_dict:
  key1: value1
  key2: value2

# Or
var_dict:
  key1: { subkey1: subvalue1, subkey2: subvalue2 }
```

## Jinja2 Templates

Variables can be used in Jinja2 templates:

```yaml
- name: Create configuration file
  template:
    src: config.j2
    dest: /etc/myapp/config.conf
```

Template file (config.j2):

```
# Configuration for {{ inventory_hostname }}
port = {{ http_port }}
max_connections = {{ max_clients }}
```

## Magic Variables

Ansible provides several built-in variables:

- `inventory_hostname`: The inventory name of the current host
- `ansible_default_ipv4.address`: The default IPv4 address
- `group_names`: List of groups the current host is in
- `groups`: Dictionary of all groups and hosts
- `hostvars`: Variables of other hosts
- `play_hosts`: List of hosts in the current play
- `inventory_file`: Path to the inventory file
- `inventory_dir`: Directory of the inventory file

## Variable Registration

Variables can be registered from task output:

```yaml
- name: Get file contents
  command: cat /etc/version
  register: version_output
- name: Display version
  debug:
    var: version_output.stdout
```

## Variable Validation

Variables can be validated using the `assert` module:

```yaml
- name: Validate variable
  assert:
    that:
      - http_port is defined
      - http_port | int > 0
      - http_port | int < 65536
    fail_msg: "http_port must be a valid port number"
    success_msg: "http_port is valid"
```

## Variable Filters

Jinja2 filters can be used to manipulate variables:

```yaml
# Convert to uppercase
{{ my_var | upper }}

# Default value if undefined
{{ my_var | default('default_value') }}
# Convert to integer
{{ my_var | int }}

# Join list items
{{ my_list | join(',') }}
# Select attribute from list of dictionaries
{{ users | selectattr('active', 'equalto', true) | list }}
```

## Secure Variables

Sensitive data should be stored using Ansible Vault:

```yaml
# In vars/vault.yml (encrypted)
---
database_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653...
```

```yaml
# In playbook
- hosts: webservers
  vars_files:
    - vars/vault.yml
  tasks:
    - name: Configure database
      mysql_user:
        name: app_user
        password: "{{ database_password }}"
```

## Conditional Variables

Variables can be conditionally assigned:

```yaml
- hosts: webservers
  vars:
    http_port: "{{ 8080 if ansible_distribution == 'CentOS' else 80 }}"
  tasks:
    - name: Configure web server
      template:
        src: httpd.conf.j2
        dest: /etc/httpd/conf/httpd.conf
```
