# Style Guide Enforcement Tools
Automated tools for enforcing coding standards and style guidelines in the Deploy-System-Unified project.

## Overview
This directory contains comprehensive tools for maintaining code quality and enforcing project standards across all components of the deployment system.

## Tools
### `enforce_style_guide.sh`
**Primary style guide enforcement script**

Comprehensive tool that checks and enforces multiple categories of standards:
#### Categories Enforced

1. **YAML Formatting Standards**
   - Trailing spaces removal
   - Proper indentation (2 spaces)
   - Line length compliance
   - Newline at end of files
   - Uses `yamllint` for validation
2. **Ansible-Specific Standards**
   - Role structure validation
   - Best practices enforcement
   - Deprecated syntax detection
   - Uses `ansible-lint` for validation

3. **Naming Conventions**
   - No spaces in filenames
   - Lowercase filenames in roles
   - Snake_case for variables
   - Auto-fixes where possible
4. **Security Standards**
   - Hardcoded secrets detection
   - Unsafe file permissions
   - SSH configuration security
   - Manual review required for security issues

5. **File Structure Standards**
   - Proper role directory structure
   - Required main.yml files
   - Consistent directory naming
## Usage

### Basic Usage
```bash
# Run full style guide enforcement
./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh
# Auto-fix all fixable issues
./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --fix

# Generate compliance report only
./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --report
# Run quietly (suppress output except errors)
./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --quiet

# Show help
./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --help
```
### Integration with Development Workflow

#### Pre-commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/sh
# Run style guide enforcement before commit
./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --fix
if [ $? -ne 0 ]; then
    echo "Style guide violations found. Please fix them before committing."
    exit 1
fi
```
#### CI/CD Pipeline
```yaml
# Example GitHub Actions workflow
- name: Enforce Style Guide
  run: |
    ./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh
```

#### Regular Maintenance
```bash
# Run weekly as part of maintenance
./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --fix
```
## Configuration

### Configuration File
`style_guide_config.json` contains project-specific configuration:
- Enabled/disabled rule categories
- Auto-fix settings
- File exclusions
- Reporting preferences
### Tool-Specific Configurations
- `.yamllint.yml` - YAML linting rules
- `.ansible-lint.yml` - Ansible linting rules

## Output
### Console Output
The script provides colored output with:
- ✅ Success messages in green
- ⚠️ Warnings in yellow
- ❌ Errors in red
- 📊 Summary statistics

### Compliance Reports
Detailed markdown reports are generated showing:
- Total issues found
- Issues auto-fixed
- Issues requiring manual attention
- Category-wise breakdown
- Recommendations
## Dependencies

Required tools (must be installed):
- `yamllint` - YAML linting
- `ansible-lint` - Ansible-specific linting
- `ripgrep` - Fast pattern matching
- `awk` - Text processing
- `sed` - Stream editing
## Best Practices

1. **Regular Execution**
   - Run before major commits
   - Include in CI/CD pipeline
   - Schedule regular maintenance runs
2. **Gradual Adoption**
   - Start with auto-fixable issues
   - Gradually enable stricter rules
   - Train team on standards

3. **Customization**
   - Adjust rules based on project needs
   - Configure exclusions for legacy code
   - Customize reporting format
4. **Integration**
   - Use with pre-commit hooks
   - Integrate with IDE/editor
   - Include in deployment pipeline

## Troubleshooting
### Common Issues

1. **Missing Dependencies**
   ```bash
   # Install required tools
   pip install yamllint ansible-lint
   sudo apt install ripgrep
   ```
2. **Permission Errors**
   ```bash
   # Make scripts executable
   chmod +x dev_tools/tools/style-guide-enforcement/*.sh
   ```

3. **Configuration Errors**
   - Check `style_guide_config.json` syntax
   - Verify tool-specific config files exist
   - Ensure paths are correct
### Getting Help

- Check the generated compliance reports
- Review tool-specific documentation
- Consult the project style guide: `LLM_RESEARCH/Style_Guide.md`
## Development

### Adding New Rules
1. Add rule logic to the appropriate enforcement function
2. Update `style_guide_config.json` with new rule
3. Update documentation
4. Test with sample violations
### Customizing Auto-fix
1. Modify the auto-fix logic in enforcement functions
2. Ensure fixes don't break functionality
3. Test thoroughly with various file types

### Extending Categories
1. Add new enforcement function
2. Integrate into main execution flow
3. Update configuration schema
4. Add appropriate tooling
## Related Documentation

- [Project Style Guide](../../LLM_RESEARCH/Style_Guide.md)
- [Architecture Documentation](../../ARCHITECTURE.md)
- [Development Tools](../../ARCHITECTURE.md#development-tools)

