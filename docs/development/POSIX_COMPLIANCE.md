# POSIX Shell Compliance Guide

## Policy

**This project enforces strict POSIX sh compliance for all shell scripts.**

We do **NOT** assume bash is available in any deployment environment. All shell scripts must be compatible with `/bin/sh` (POSIX sh).

## Rationale

1. **Portability**: POSIX sh is available on all Unix-like systems
2. **Minimal environments**: Many containers and embedded systems don't have bash
3. **Security**: Smaller attack surface than bash
4. **Performance**: POSIX sh is typically faster and uses less memory

## Enforcement

### Pre-commit Hook
All `.sh` files are checked by `shellcheck -s sh` before commit.

### CI/CD
The `style-enforcement.yml` workflow fails if POSIX compliance issues are detected.

### Auto-fix
The `enforce_style_guide.sh --fix` command can automatically fix:
- Non-POSIX shebangs (`#!/bin/bash` → `#!/bin/sh`)
- Some POSIX compatibility issues

## Bash → POSIX sh Migration Guide

### ❌ Bash-specific (NOT ALLOWED) → ✅ POSIX-compliant (REQUIRED)

#### 1. Shebang
```bash
# ❌ NOT ALLOWED
#!/bin/bash
#!/usr/bin/env bash

# ✅ REQUIRED
#!/bin/sh
```

#### 2. Arrays
```bash
# ❌ NOT ALLOWED
my_array=(one two three)
echo "${my_array[0]}"

# ✅ REQUIRED
item1="one"
item2="two"
item3="three"
# or use positional parameters
set -- one two three
echo "$1"
```

#### 3. Conditional Expressions
```bash
# ❌ NOT ALLOWED
[[ -z "$var" ]]
[[ "$a" == "$b" ]]

# ✅ REQUIRED
[ -z "$var" ]
[ "$a" = "$b" ]
```

#### 4. Parameter Expansion
```bash
# ❌ NOT ALLOWED
${var^^}           # Uppercase
${var,,}           # Lowercase
${var:0:5}         # Substring
${var//pattern/rep} # Global replace

# ✅ REQUIRED
echo "$var" | tr '[:lower:]' '[:upper:]'
echo "$var" | tr '[:upper:]' '[:lower:]'
echo "$var" | cut -c1-5
# Use sed for replacements
echo "$var" | sed 's/pattern/rep/g'
```

#### 5. Arithmetic
```bash
# ❌ NOT ALLOWED
((count++))
let "result = a + b"

# ✅ REQUIRED
count=$((count + 1))
result=$((a + b))
```

#### 6. Functions
```bash
# ❌ NOT ALLOWED
function my_func() {
    # ...
}

# ✅ REQUIRED
my_func() {
    # ...
}
```

#### 7. Command Substitution
```bash
# ❌ AVOID (bashism, but works in most sh)
var=`command`

# ✅ PREFERRED
var=$(command)
```

#### 8. Case Statements
```bash
# ❌ NOT ALLOWED
case "$var" in
    +([0-9])) ;;  # Extended glob
esac

# ✅ REQUIRED
case "$var" in
    *[0-9]*) ;;   # POSIX pattern
esac
```

#### 9. Here Strings
```bash
# ❌ NOT ALLOWED
grep pattern <<< "$input"

# ✅ REQUIRED
echo "$input" | grep pattern
```

#### 10. Process Substitution
```bash
# ❌ NOT ALLOWED
diff <(sort file1) <(sort file2)

# ✅ REQUIRED
sort file1 > /tmp/sorted1
sort file2 > /tmp/sorted2
diff /tmp/sorted1 /tmp/sorted2
rm /tmp/sorted1 /tmp/sorted2
```

## Common POSIX Patterns

### Looping
```sh
# For loops
for item in $list; do
    echo "$item"
done

# While loops
while [ -n "$input" ]; do
    # ...
done

# Until loops
until [ -f "$file" ]; do
    sleep 1
done
```

### Conditionals
```sh
# Simple if
if [ -f "$file" ]; then
    echo "File exists"
fi

# If-else
if [ "$var" = "value" ]; then
    echo "Match"
else
    echo "No match"
fi

# Nested
if [ -d "$dir" ]; then
    if [ -r "$dir" ]; then
        echo "Readable directory"
    fi
fi
```

### Functions
```sh
# Define
log_message() {
    level="$1"
    message="$2"
    echo "[$level] $message"
}

# Call
log_message "INFO" "Starting process"

# Return values
check_file() {
    [ -f "$1" ]
}

if check_file "/etc/passwd"; then
    echo "File exists"
fi
```

## Testing POSIX Compliance

### Manual Check
```bash
shellcheck -s sh script.sh
```

### Run Full Audit
```bash
./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --report
```

### Pre-commit Test
```bash
pre-commit run shellcheck --all-files
```

## Ansible Integration

Embedded shell scripts in Ansible tasks must also be POSIX-compliant:

```yaml
- name: POSIX-compliant shell command
  ansible.builtin.shell: |
    #!/bin/sh
    set -e
    if [ -f "/etc/os-release" ]; then
      . /etc/os-release
      echo "Running on $ID"
    fi
  args:
    executable: /bin/sh
```

**Note**: Always specify `executable: /bin/sh` in Ansible shell tasks.

## Exceptions

No exceptions are allowed. If a script requires bash-specific features:
1. Document why POSIX is insufficient
2. Add bash as an explicit dependency
3. Tag the script with `# bash-required` comment
4. Exclude from POSIX enforcement in `.shellcheckrc`

## References

- [POSIX Shell Specification](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck Wiki - POSIX](https://github.com/koalaman/shellcheck/wiki/ShellCheck-Warnings#posh-portability-warnings)
- [Debian Policy Manual - Shell Scripts](https://www.debian.org/doc/debian-policy/ch-opersys.html#shell-scripts)

## Questions?

Open an issue if you encounter POSIX compatibility challenges or need clarification on specific constructs.
