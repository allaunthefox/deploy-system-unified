# STYLE_GUIDE

To maintain consistency and ensure clean linting across the Deploy-System-Unified project, all contributions must adhere to the following style requirements. These standards are enforced via the `make lint` suite.

## Style Guide Categories

For detailed style requirements, see the specific guides:

<<<<<<< HEAD
* **[YAML Style Guide](DEV_STYLE_YAML_STYLE_GUIDE)**: Standards for YAML files including proper formatting and syntax
* **[Ansible Style Guide](DEV_STYLE_ANSIBLE_STYLE_GUIDE)**: Best practices for Ansible playbooks and roles
* **[Shell Style Guide](DEV_STYLE_SHELL_STYLE_GUIDE)**: Requirements for shell scripts and command-line tools
* **[Documentation Style Guide](DEV_STYLE_DOCUMENTATION_STYLE_GUIDE)**: Guidelines for documentation and markdown files
=======
* **[YAML Style Guide](DEV_STYLE_YAML_Style_Guide)**: Standards for YAML files including proper formatting and syntax
* **[Ansible Style Guide](DEV_STYLE_Ansible_Style_Guide)**: Best practices for Ansible playbooks and roles
* **[Shell Style Guide](DEV_STYLE_Shell_Style_Guide)**: Requirements for shell scripts and command-line tools
* **[Documentation Style Guide](DEV_STYLE_Documentation_Style_Guide)**: Guidelines for documentation and markdown files
>>>>>>> c42ffcf4 (Rename wiki pages to SCREAMING_SNAKE_CASE convention)

## General Standards

* **Extensions**: Use `.yml` for all YAML files, not `.yaml`.
* **EOF Newlines**: Every file (YAML, Markdown, Jinja2, etc.) must end with exactly one newline character.
* **Trailing Whitespace**: No lines should have trailing spaces or tabs.
* **Indentation**: Use spaces for indentation, never tabs.