# YAML Formatting Fix Scripts

This directory contains automated scripts to fix YAML formatting violations in the Deploy-System-Unified project.

## Scripts

### `fix_yaml_formatting.sh`
Comprehensive script that fixes:
- Trailing spaces in YAML files
- Systematic indentation issues (4 spaces → 2 spaces)
- Empty lines with only whitespace

### `fix_trailing_spaces_and_newlines.sh`
Targeted script for specific issues:
- Files with trailing spaces and missing newlines
- Long lines that exceed character limits
- Syntax errors in YAML files

## Usage

```bash
# Run comprehensive fixes
./dev_tools/scripts/yaml-fixes/fix_yaml_formatting.sh

# Run targeted fixes for remaining issues
./dev_tools/scripts/yaml-fixes/fix_trailing_spaces_and_newlines.sh

# Validate results
find roles/ -name "*.yml" -exec yamllint {} \; 2>&1 | grep -E "(error|warning)" || echo "✅ No YAML formatting issues found"
```

## Files Fixed

- `roles/security/advanced/tasks/main.yml`
- `roles/security/scanning/tasks/main.yml`
- All security scanning task files in `roles/security/scanning/tasks/`

## Validation

After running the scripts, validate the fixes with:
```bash
yamllint roles/
```

The project should show no YAML formatting errors or warnings.
