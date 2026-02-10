# overview

This directory contains documentation for Ansible, based on the current official documentation from the Ansible project.

## Core Concepts

### Playbooks

Playbooks are Ansible's configuration, deployment, and orchestration language. They can describe a policy you want your remote systems to enforce, or a set of steps in a general IT workflow.

### Inventory

Inventory is a list of managed nodes (hosts) that Ansible can connect to and manage. It can be static (INI-style) or dynamic (script-generated).

### Modules

Modules are the units of work in Ansible. Each module is a standalone script that can be invoked by the Ansible API, or by the `ansible` or `ansible-playbook` programs.

### Variables

Variables are used to store values that can be reused throughout playbooks and roles. They allow for abstraction and customization of playbooks.

### Facts

Facts are information derived from speaking with your remote systems, including network interfaces, operating system, and more.

### Handlers

Handlers are special tasks that run only when notified by other tasks.

### Roles

Roles are a way to automatically load certain variables, tasks, and handlers based on a known file structure.

## Configuration

### ansible.cfg

The main configuration file for Ansible, which can be placed in multiple locations with different precedence levels.

### Environment Variables

Ansible can be configured using environment variables, which take precedence over configuration file settings.

## Execution

### Ad-hoc Commands

Single tasks executed using the `ansible` command.

### Playbook Execution

Multi-task operations executed using the `ansible-playbook` command.

## Security

### Ansible Vault

A feature for managing sensitive data like passwords, keys, and other secrets.

### Privilege Escalation

Mechanisms for running tasks with elevated privileges using `become`.

## Best Practices

### Directory Layout

Recommended project structure for organizing playbooks, roles, and other files.

### Variable Management

Best practices for defining and using variables.

### Error Handling

Strategies for handling errors and failures in playbooks.

### Testing

Methods for testing playbooks and roles.
