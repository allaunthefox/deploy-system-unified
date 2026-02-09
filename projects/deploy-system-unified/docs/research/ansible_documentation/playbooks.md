# Ansible Playbooks

Playbooks are Ansible's configuration, deployment, and orchestration language. They can describe a policy you want your remote systems to enforce, or a set of steps in a general IT workflow.

## Structure

Playbooks are written in YAML format and consist of one or more 'plays' in a list.

```yaml
---
- name: Install and configure web servers
  hosts: webservers
  become: true
  vars:
    http_port: 80
  tasks:
    - name: Ensure apache is installed
      package:
        name: apache2
        state: present

    - name: Ensure apache is running
      service:
        name: apache2
        state: started
        enabled: true
```

## Plays

A play is an ordered set of tasks to be applied to hosts selected by an inventory.

### Key Components

- `hosts`: Defines the host pattern for the play
- `name`: Human-readable description of the play
- `tasks`: List of tasks to execute
- `vars`: Variables for the play
- `handlers`: Handlers for the play
- `roles`: Roles to apply to the hosts

## Tasks

Tasks are the units of action in Ansible. Each task calls a module.

### Task Attributes

- `name`: Descriptive name for the task
- `module`: The module to call
- `args`: Arguments to pass to the module
- `when`: Conditional execution
- `loop`: Iterate over a list
- `register`: Save output to a variable
- `notify`: Notify handlers

## Variables

Variables in Ansible can come from multiple sources with different precedence levels.

### Variable Precedence (Highest to Lowest)

1. Extras vars (-e/--extra-vars)
2. Task vars
3. Block vars
4. Role and include vars
5. Play vars_files
6. Play vars_prompt
7. Play vars
8. Host facts
9. Host vars
10. Group vars
11. Role defaults

## Conditionals

Conditionals allow you to control the execution of tasks based on certain conditions.

```yaml
- name: Install nginx on Ubuntu
  apt:
    name: nginx
    state: present
  when: ansible_distribution == "Ubuntu"
```

## Loops

Loops allow you to repeat tasks multiple times with different values.

```yaml
- name: Install multiple packages
  package:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - apache2
    - php
```

## Handlers

Handlers are special tasks that run only when notified by other tasks.

```yaml
- name: Copy nginx config
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
  notify: restart nginx
handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted
```

## Tags

Tags allow you to run specific parts of a playbook.

```yaml
- name: Install nginx
  apt:
    name: nginx
    state: present
  tags:
    - web
    - install
```

## Error Handling

Ansible provides several mechanisms for error handling:

- `ignore_errors`: Continue execution despite task failure
- `failed_when`: Define custom failure conditions
- `block/rescue/always`: Exception handling blocks
