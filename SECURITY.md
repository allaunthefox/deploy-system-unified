# Security Policy

## Supported Versions

The following versions of this project are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < latest| :x:                |

We recommend always using the latest version to ensure you have the most recent security patches.

## Reporting a Vulnerability

I take the security of this project seriously. If you discover a security vulnerability, please follow these steps:

### **DO NOT** disclose the vulnerability publicly

- **Do not** create a public GitHub issue
- **Do not** discuss the vulnerability in public channels
- **Do not** share the vulnerability with others before it is resolved

### How to Report

1. **Create a draft security advisory** in the GitHub Security tab, or
2. **Email me directly** at bigdataiscoming+9i37y6j2@protonmail.com

### What to Include

Please provide as much information as possible:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if you have one)
- Your contact information for follow-up questions

### Response Timeline

- **Acknowledgment**: I will acknowledge receipt of your report within **48 hours**
- **Initial Assessment**: I will provide an initial assessment within **5 business days**
- **Resolution**: I aim to resolve critical vulnerabilities within **30 days**

### What to Expect

1. **Confirmation**: I will confirm whether I can reproduce the issue
2. **Updates**: You will receive updates on the progress at least every 14 days
3. **Disclosure**: Once resolved, I will coordinate responsible disclosure with you
4. **Credit**: With your permission, I will acknowledge your contribution in the security advisory

## Security Best Practices for Contributors

When contributing to this project, please follow these security guidelines:

### Ansible-Specific Security

- **Never commit secrets**: Use Ansible Vault for sensitive data
- **Validate inputs**: Sanitize all variables that could be user-controlled
- **Use official modules**: Prefer official Ansible modules over shell commands
- **Pin versions**: Specify exact versions for dependencies
- **Review permissions**: Ensure tasks run with minimal required privileges

### General Security

- **Keep dependencies updated**: Regularly update and patch dependencies
- **Follow least privilege**: Grant only necessary permissions
- **Validate configurations**: Use ansible-lint and security scanning tools
- **Document security implications**: Note security-related changes in PR descriptions

## Security Tools

This project uses the following security tools:

- **ansible-lint**: For Ansible best practices
- **yamllint**: For YAML syntax validation
- **Secret detection**: Pre-commit hooks to prevent secret commits
- **Dependency scanning**: Automated vulnerability scanning

## Known Security Considerations

### Vault Secrets

- Always encrypt sensitive variables with Ansible Vault
- Never store vault passwords in the repository
- Rotate vault passwords periodically

### Privilege Escalation

- Use `become` only when necessary
- Document why privilege escalation is required
- Limit scope of privileged tasks

### Network Security

- Validate all network configurations
- Use TLS/SSL for remote connections
- Implement proper firewall rules

## Contact

For security-related questions or concerns, please contact me:

- **Email**: bigdataiscoming+9i37y6j2@protonmail.com
- **GitHub Security Advisories**: Enable in repository settings

---

*This security policy is subject to change. Please check back regularly for updates.*
