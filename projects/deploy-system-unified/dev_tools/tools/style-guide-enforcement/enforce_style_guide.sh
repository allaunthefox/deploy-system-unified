#!/usr/bin/env bash

# Deploy-System-Unified Style Guide Enforcement Tool
# Comprehensive script to enforce project coding standards

set -e
set -o pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
YAML_LINT_CONFIG="$PROJECT_ROOT/.yamllint.yml"
ANSIBLE_LINT_CONFIG="$PROJECT_ROOT/.ansible-lint.yml"
STYLE_GUIDE="$PROJECT_ROOT/LLM_RESEARCH/Style_Guide.md"
STYLE_IGNORE="$PROJECT_ROOT/dev_tools/tools/style-guide-enforcement/.styleignore"

# Check style ignore patterns (supports glob patterns, negation with '!pattern', and regex using 're:pattern')
# Behavior: patterns are applied in file order. A match sets ignored=true; a
# later negation '!pattern' can unset it. Regex patterns are prefixed with 're:'.
is_ignored() {
    local path="$1"
    [ ! -f "$STYLE_IGNORE" ] && return 1

    local ignored=0
    local line
    while IFS= read -r line || [ -n "$line" ]; do
        # Strip trailing CR if present
        line="${line%$'\r'}"
        # Skip blank lines and comments
        [[ -z "${line//[[:space:]]/}" ]] && continue
        [[ "${line:0:1}" == "#" ]] && continue

        local neg=0
        local pat="$line"
        if [[ "${pat:0:1}" == "!" ]]; then
            neg=1
            pat="${pat:1}"
        fi

        if [[ "$pat" == re:* ]]; then
            local regex="${pat#re:}"
            if printf '%s' "$path" | grep -Eq -- "$regex"; then
                if [ $neg -eq 1 ]; then
                    ignored=0
                else
                    ignored=1
                fi
            fi
        else
            # Shell glob match using case (preserves glob semantics)
            # shellcheck disable=SC2254
            case "$path" in
                $pat)
                    if [ $neg -eq 1 ]; then
                        ignored=0
                    else
                        ignored=1
                    fi
                    ;;
            esac
        fi
    done < "$STYLE_IGNORE"

    [ $ignored -eq 1 ] && return 0 || return 1
}

# Counters
TOTAL_ISSUES=0
FIXED_ISSUES=0

# Flags
AUTO_FIX=false
LOW_RISK_REPAIR=false
REPORT_ONLY=false

# Logging functions
log() { echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

# Perform "hard to fail" safe repairs
perform_safe_repairs() {
    local file="$1"
    local fixed=0

    # 1. Fix trailing spaces
    if grep -q "[[:space:]]$" "$file"; then
        sed -i 's/[[:space:]]*$//' "$file"
        fixed=1
    fi

    # 2. Ensure file ends with newline
    if [ -s "$file" ] && [ "$(tail -c 1 "$file" | wc -l)" -eq 0 ]; then
        echo "" >> "$file"
        fixed=1
    fi

    # 3. Add YAML document start '---' if missing (only for .yml/.yaml)
    if [[ "$file" =~ \.ya?ml$ ]]; then
        if ! awk 'NF{print;exit}' "$file" | grep -qE '^---'; then
            sed -i '1s/^/---\n/' "$file"
            fixed=1
        fi
    fi

    if [ $fixed -eq 1 ]; then
        FIXED_ISSUES=$((FIXED_ISSUES + 1))
        return 0
    else
        return 1
    fi
}

# Check if required tools are installed
check_dependencies() {
    log "Checking dependencies..."
    
    local missing_tools=()
    
    command -v yamllint >/dev/null 2>&1 || missing_tools+=("yamllint")
    command -v ansible-lint >/dev/null 2>&1 || missing_tools+=("ansible-lint")
    command -v awk >/dev/null 2>&1 || missing_tools+=("awk")
    command -v sed >/dev/null 2>&1 || missing_tools+=("sed")
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        error "Missing required tools: ${missing_tools[*]}"
        error "Please install the missing tools and try again."
        exit 1
    fi

    if command -v rg >/dev/null 2>&1; then
        success "All dependencies available (including ripgrep)"
    else
        warning "ripgrep not found, falling back to standard grep (processing may be slower)"
    fi

    if command -v fd >/dev/null 2>&1 || command -v fdfind >/dev/null 2>&1; then
        success "All dependencies available (including fd)"
    else
        warning "fd not found, falling back to standard find (processing may be slower)"
    fi

    if command -v shellcheck >/dev/null 2>&1; then
        success "All dependencies available (including shellcheck)"
    else
        warning "shellcheck not found, internal shell scripts will not be audited"
    fi
}

# Enforce YAML formatting standards
enforce_yaml_standards() {
    log "Enforcing YAML formatting standards..."
    
    local yaml_files=()
    local fd_cmd=""
    if command -v fd >/dev/null 2>&1; then fd_cmd="fd"; elif command -v fdfind >/dev/null 2>&1; then fd_cmd="fdfind"; fi

    if [ -n "$fd_cmd" ]; then
        while IFS= read -r file; do
            yaml_files+=("$file")
        done < <("$fd_cmd" . "$PROJECT_ROOT" -e yml -e yaml --exclude .git)
    else
        while IFS= read -r -d '' file; do
            yaml_files+=("$file")
        done < <(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -print0)
    fi
    
    if [ ${#yaml_files[@]} -eq 0 ]; then
        warning "No YAML files found"
        return 0
    fi
    
    # Run yamllint
    if [ -f "$YAML_LINT_CONFIG" ]; then
        log "Running yamllint with project configuration..."
        if yamllint -c "$YAML_LINT_CONFIG" "${yaml_files[@]}" 2>&1 | tee /tmp/yamllint_output.txt; then
            success "YAML formatting standards met"
        else
            warning "YAML linting found issues"
            local issue_count
            issue_count=$(grep -E -c "error|warning" /tmp/yamllint_output.txt || echo 0)
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
            
            # Auto-fix or Low-Risk Repair
            if [ "$AUTO_FIX" = true ] || [ "$LOW_RISK_REPAIR" = true ]; then
                log "Applying safe repairs to YAML files..."
                for file in "${yaml_files[@]}"; do
                    perform_safe_repairs "$file" || true
                    
                    # More aggressive fixes only for AUTO_FIX
                    if [ "$AUTO_FIX" = true ]; then
                        # Normalize common boolean values (True/False/Yes/No) to lowercase true/false
                        perl -i -pe 's/(:\s*)(True|False|TRUE|FALSE|Yes|No|YES|NO|yes|no)\b/$1 . lc($2)/ge' "$file"
                        # Remove unnecessary spaces inside square brackets
                        perl -i -0777 -pe 's/\[\s*([^\[\]]*?)\s*\]/[\1]/g' "$file"
                    fi
                done
                success "YAML repairs complete"
            fi
        fi
    else
        log "Running yamllint with default configuration..."
        if yamllint "${yaml_files[@]}" 2>&1 | tee /tmp/yamllint_output.txt; then
            success "YAML formatting standards met"
        else
            warning "YAML linting found issues"
            local issue_count
            issue_count=$(grep -E -c "error|warning" /tmp/yamllint_output.txt || echo 0)
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi
}

# Enforce Ansible-specific standards
enforce_ansible_standards() {
    log "Enforcing Ansible-specific standards..."
    
    local ansible_files=()
    local fd_cmd=""
    if command -v fd >/dev/null 2>&1; then fd_cmd="fd"; elif command -v fdfind >/dev/null 2>&1; then fd_cmd="fdfind"; fi

    if [ -n "$fd_cmd" ]; then
        while IFS= read -r file; do
            ansible_files+=("$file")
        done < <("$fd_cmd" . "$PROJECT_ROOT/roles" -e yml --exclude .git)
    else
        while IFS= read -r -d '' file; do
            ansible_files+=("$file")
        done < <(find "$PROJECT_ROOT/roles" -name "*.yml" -not -path "*/.git/*" -print0)
    fi
    
    if [ ${#ansible_files[@]} -eq 0 ]; then
        warning "No Ansible role files found"
        return 0
    fi
    
    # Run ansible-lint
    if [ -f "$ANSIBLE_LINT_CONFIG" ]; then
        log "Running ansible-lint with project configuration..."
        if ansible-lint -c "$ANSIBLE_LINT_CONFIG" "${ansible_files[@]}" 2>&1 | tee /tmp/ansible_lint_output.txt; then
            success "Ansible standards met"
        else
            warning "Ansible linting found issues"
            local issue_count
            issue_count=$(grep -E -c "error|warning" /tmp/ansible_lint_output.txt || echo 0)
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    else
        log "Running ansible-lint with default configuration..."
        if ansible-lint "${ansible_files[@]}" 2>&1 | tee /tmp/ansible_lint_output.txt; then
            success "Ansible standards met"
        else
            warning "Ansible linting found issues"
            local issue_count
            issue_count=$(grep -E -c "error|warning" /tmp/ansible_lint_output.txt || echo 0)
            TOTAL_ISSUES=$((TOTAL_ISSUES + issue_count))
        fi
    fi
}

# Enforce FQCN (Fully Qualified Collection Names)
enforce_fqcn_standards() {
    log "Enforcing FQCN standards..."

    local short_form_matches=()
    # Use a PCRE that matches module names only when used as top-level task entries,
    # either directly under '-' or after '- name:', to avoid matching parameter keys like 'group:'
    local better_pattern='(?s)(-\s+name:.*?\n\s{2,}(?:apt|dnf|copy|template|service|systemd|shell|command|stat|mount|cron|assert|debug|set_fact|include_tasks|import_tasks|import_role|include_role):)|(^-\s+(?:apt|dnf|copy|template|service|systemd|shell|command|stat|mount|cron|assert|debug|set_fact|include_tasks|import_tasks|import_role|include_role):)'

    if command -v rg >/dev/null 2>&1; then
        while IFS= read -r file; do
            short_form_matches+=("$file")
        done < <(rg -P -U --no-ignore -l "$better_pattern" -g "roles/**/tasks/**/*.yml" -g "roles/**/tasks/*.yml" -g "roles/**/handlers/**/*.yml" -g "roles/**/handlers/*.yml" -g "roles/**/meta/**/*.yml" -g "roles/**/meta/*.yml" --glob "!.git/*" "$PROJECT_ROOT" 2>/dev/null)
    else
        while IFS= read -r file; do
            short_form_matches+=("$file")
        done < <(find "$PROJECT_ROOT/roles" -type f \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec grep -lE "$better_pattern" {} \; 2>/dev/null)
    fi

    # Filter out ignored files and non-playbook config files like molecule configs
    local filtered_matches=()
    for file in "${short_form_matches[@]}"; do
        local relative_path
        relative_path=$(realpath --relative-to="$PROJECT_ROOT" "$file")
        # Ignore molecule directories (molecule configs are not Ansible tasks)
        if [[ "$relative_path" == */molecule/* || "$relative_path" == molecule/* ]]; then
            continue
        fi
        if ! is_ignored "$relative_path"; then
            filtered_matches+=("$file")
        fi
    done

    if [ ${#filtered_matches[@]} -gt 0 ]; then
        warning "Found ${#filtered_matches[@]} file(s) with potential non-FQCN module calls"
        for file in "${filtered_matches[@]}"; do
            warning "  - $file"
        done
        TOTAL_ISSUES=$((TOTAL_ISSUES + ${#filtered_matches[@]}))
    fi

    success "FQCN standards checked"
}

# Enforce shell script standards
enforce_shell_standards() {
    log "Enforcing shell script standards..."
    
    if ! command -v shellcheck >/dev/null 2>&1;
 then
        warning "shellcheck not found, skipping shell audit"
        return 0
    fi

    local shell_files=()
    local fd_cmd=""
    if command -v fd >/dev/null 2>&1; then fd_cmd="fd"; elif command -v fdfind >/dev/null 2>&1; then fd_cmd="fdfind"; fi

    if [ -n "$fd_cmd" ]; then
        while IFS= read -r file; do shell_files+=("$file"); done < <("$fd_cmd" . "$PROJECT_ROOT" -e sh --exclude .git)
    else
        while IFS= read -r -d '' file; do shell_files+=("$file"); done < <(find "$PROJECT_ROOT" -name "*.sh" -not -path "*/.git/*" -print0)
    fi

    # 1. Audit standalone .sh files
    for file in "${shell_files[@]}"; do
        # Check specific architectural compatibility (#!/usr/bin/env bash)
        if head -n 1 "$file" | grep -q "^#!/bin/bash$"; then
            warning "Compatibility Issue: $file uses '#!/bin/bash'. Recommend '#!/usr/bin/env bash' for cross-platform support."
            TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
            
            if [ "$AUTO_FIX" = true ] || [ "$LOW_RISK_REPAIR" = true ]; then
                 log "Fixing shebang in $file..."
                 sed -i 's|^#!/bin/bash$|#!/usr/bin/env bash|' "$file"
                 FIXED_ISSUES=$((FIXED_ISSUES + 1))
            fi
        fi

        # Run ShellCheck with architectural awareness checks
        # SC2039: In POSIX sh, something is undefined. (Ignored as we assume bash-compatible env)
        # SC3000-SC3999: Checks specific to shells (we want these)
        if ! shellcheck -x -e SC2039 "$file"; then
            warning "shellcheck found issues in standalone script: $file"
            TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
        fi
    done

    # 2. Audit embedded shell blocks in YAML
    log "Auditing embedded shell blocks in Ansible tasks..."
    local yaml_files=()
    if [ -n "$fd_cmd" ]; then
        while IFS= read -r file; do yaml_files+=("$file"); done < <("$fd_cmd" . "$PROJECT_ROOT/roles" -e yml -e yaml --exclude .git)
    else
        while IFS= read -r -d '' file; do yaml_files+=("$file"); done < <(find "$PROJECT_ROOT/roles" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -print0)
    fi

    for file in "${yaml_files[@]}"; do
        awk '/shell: \|/,/^  [^ ]/' "$file" | grep -v "shell: |" | grep -v "^  -" > /tmp/embedded_shell.sh || true
        
        if [ -s /tmp/embedded_shell.sh ]; then
            sed -i '1s/^/#!\/bin\/bash\n/' /tmp/embedded_shell.sh
            if ! shellcheck -s bash /tmp/embedded_shell.sh > /dev/null 2>&1;
 then
                if shellcheck -s bash /tmp/embedded_shell.sh 2>&1 | grep -qvE "SC1083|SC2086|SC2050"; then
                    warning "Potential shell logic issue in embedded block: $file"
                    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
                fi
            fi
        fi
    done
    
    success "Shell standards checked"
}

# Enforce naming conventions
enforce_naming_conventions() {
    log "Enforcing naming conventions..."
    
    local fd_cmd=""
    if command -v fd >/dev/null 2>&1; then fd_cmd="fd"; elif command -v fdfind >/dev/null 2>&1; then fd_cmd="fdfind"; fi

    # Check for files with spaces in names
    local files_with_spaces=()
    if [ -n "$fd_cmd" ]; then
        while IFS= read -r file;
 do
            files_with_spaces+=("$file")
        done < <("$fd_cmd" -g "* *" "$PROJECT_ROOT" --exclude .git)
    else
        while IFS= read -r -d '' file;
 do
            files_with_spaces+=("$file")
        done < <(find "$PROJECT_ROOT" -name "* *" -not -path "*/.git/*" -print0 2>/dev/null)
    fi
    
    if [ ${#files_with_spaces[@]} -gt 0 ]; then
        warning "Found ${#files_with_spaces[@]} files with spaces in names"
        TOTAL_ISSUES=$((TOTAL_ISSUES + ${#files_with_spaces[@]}))
        
        # Renaming is a structural change, only done in AUTO_FIX, NOT LOW_RISK_REPAIR
        if [ "$AUTO_FIX" = true ]; then
            for file in "${files_with_spaces[@]}"; do
                local dir
                dir=$(dirname "$file")
                local base
                base=$(basename "$file")
                local new_name="${base// /_}"
                warning "Renaming: $base -> $new_name"
                mv "$file" "$dir/$new_name"
                FIXED_ISSUES=$((FIXED_ISSUES + 1))
            done
        fi
    fi
    
    # Check for uppercase filenames in roles
    local uppercase_files=()
    if [ -d "$PROJECT_ROOT/roles" ]; then
        if [ -n "$fd_cmd" ]; then
            while IFS= read -r file;
 do
                uppercase_files+=("$file")
            done < <("$fd_cmd" -t f -g "[A-Z]*" "$PROJECT_ROOT/roles" --exclude .git)
        else
            while IFS= read -r -d '' file;
 do
                local base
                base=$(basename "$file")
                if [[ "$base" =~ ^[A-Z] ]]; then
                    uppercase_files+=("$file")
                fi
            done < <(find "$PROJECT_ROOT/roles" -type f -not -path "*/.git/*" -print0 2>/dev/null)
        fi
    fi
    
    if [ ${#uppercase_files[@]} -gt 0 ]; then
        warning "Found ${#uppercase_files[@]} files with uppercase names in roles directory"
        TOTAL_ISSUES=$((TOTAL_ISSUES + ${#uppercase_files[@]}))
        
        if [ "$AUTO_FIX" = true ]; then
            for file in "${uppercase_files[@]}"; do
                local dir
                dir=$(dirname "$file")
                local base
                base=$(basename "$file")
                local new_name
                new_name=$(echo "$base" | tr '[:upper:]' '[:lower:]')
                if [ "$base" != "$new_name" ]; then
                    warning "Renaming: $base -> $new_name"
                    mv "$file" "$dir/$new_name"
                    FIXED_ISSUES=$((FIXED_ISSUES + 1))
                fi
            done
        fi
    fi
    
    success "Naming conventions enforced"
}

# Enforce file structure standards
enforce_file_structure() {
    log "Enforcing file structure standards..."
    
    local roles_dir="$PROJECT_ROOT/roles"
    if [ ! -d "$roles_dir" ]; then
        success "No roles directory found"
        return 0
    fi

    local fd_cmd=""
    if command -v fd >/dev/null 2>&1; then fd_cmd="fd"; elif command -v fdfind >/dev/null 2>&1; then fd_cmd="fdfind"; fi

    local role_paths=()
    if [ -n "$fd_cmd" ]; then
        while IFS= read -r dir;
 do
            role_paths+=("$dir")
        done < <("$fd_cmd" -t d -H "^(tasks|handlers|defaults|vars)$" "$roles_dir" --exclude .git | xargs -I{} dirname {} | sort -u)
    else
        while IFS= read -r -d '' dir;
 do
            role_paths+=("$dir")
        done < <(find "$roles_dir" -type d \( -name tasks -o -name handlers -o -name defaults -o -name vars \) -not -path "*/.git/*" -print0 | xargs -0 -I{} dirname {} | sort -u | tr '\n' '\0')
    fi

    for role_path in "${role_paths[@]}"; do
        local role_name
        role_name=$(realpath --relative-to="$roles_dir" "$role_path")
        local relative_path
        relative_path=$(realpath --relative-to="$PROJECT_ROOT" "$role_path")

        if is_ignored "$relative_path"; then
            log "Skipping ignored path: $relative_path"
            continue
        fi
        
        for dir in "tasks" "handlers" "defaults" "vars" "templates" "files"; do
            if [ ! -d "$role_path/$dir" ]; then
                warning "Role '$role_name' missing '$dir' directory"
                TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
            fi
        done
        
        for main_file in "tasks/main.yml" "handlers/main.yml" "defaults/main.yml" "vars/main.yml"; do
            if [ ! -f "$role_path/$main_file" ]; then
                warning "Role '$role_name' missing '$main_file'"
                TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
            fi
        done
    done
    
    success "File structure standards checked"
}

# Enforce security standards
enforce_security_standards() {
    log "Enforcing security standards..."
    
    local secret_patterns=(
        'password[[:space:]]*[:=]'
        'secret[[:space:]]*[:=]'
        'token[[:space:]]*[:=]'
        'api_key[[:space:]]*[:=]'
        'private_key[[:space:]]*[:=]'
    )
    
    local fd_cmd=""
    if command -v fd >/dev/null 2>&1; then fd_cmd="fd"; elif command -v fdfind >/dev/null 2>&1; then fd_cmd="fdfind"; fi

    for pattern in "${secret_patterns[@]}"; do
        local matches=()
        local candidates=()
        
        if command -v rg >/dev/null 2>&1;
 then
            while IFS= read -r file;
 do
                candidates+=("$file")
            done < <(rg -l -e "$pattern" -g "*.yml" -g "*.yaml" --glob "!.git/*" "$PROJECT_ROOT" 2>/dev/null)
        elif [ -n "$fd_cmd" ]; then
            while IFS= read -r file;
 do
                candidates+=("$file")
            done < <("$fd_cmd" . "$PROJECT_ROOT" -e yml -e yaml --exclude .git -x grep -l -E "$pattern" 2>/dev/null)
        else
            while IFS= read -r file;
 do
                candidates+=("$file")
            done < <(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec grep -l -E "$pattern" {} \; 2>/dev/null)
        fi

        for file in "${candidates[@]}"; do
             if is_ignored "$(realpath --relative-to="$PROJECT_ROOT" "$file")"; then
                 continue
             fi
             
             if grep -E "$pattern" "$file" | grep -qv "{{"; then
                  matches+=("$file")
             fi
        done
        
        if [ ${#matches[@]} -gt 0 ]; then
            warning "Found ${#matches[@]} file(s) with potential hardcoded secrets matching pattern: $pattern"
            for file in "${matches[@]}"; do
                warning "  - $file"
            done
            TOTAL_ISSUES=$((TOTAL_ISSUES + ${#matches[@]}))
        fi
    done
    
    local unsafe_perms=()
    local perm_pattern='mode:\s*['\''"]?(0?777|0?666)['\''"]?'
    
    if command -v rg >/dev/null 2>&1;
 then
        while IFS= read -r file;
 do
            unsafe_perms+=("$file")
        done < <(rg -l "$perm_pattern" -g "*.yml" -g "*.yaml" --glob "!.git/*" "$PROJECT_ROOT" 2>/dev/null)
    elif [ -n "$fd_cmd" ]; then
        while IFS= read -r file;
 do
            unsafe_perms+=("$file")
        done < <("$fd_cmd" . "$PROJECT_ROOT" -e yml -e yaml --exclude .git -x grep -l "$perm_pattern" 2>/dev/null)
    else
        while IFS= read -r file;
 do
            unsafe_perms+=("$file")
        done < <(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec grep -l "$perm_pattern" {} \; 2>/dev/null)
    fi
    
    if [ ${#unsafe_perms[@]} -gt 0 ]; then
        warning "Found ${#unsafe_perms[@]} file(s) with potentially unsafe permissions (777/666)"
        for file in "${unsafe_perms[@]}"; do
            warning "  - $file"
        done
        TOTAL_ISSUES=$((TOTAL_ISSUES + ${#unsafe_perms[@]}))
    fi
    
    success "Security standards checked"
}

# Generate style guide compliance report
generate_report() {
    log "Generating style guide compliance report..."
    
    local report_file
    report_file="$PROJECT_ROOT/dev_tools/tools/style-guide-enforcement/compliance_report_$(date +%Y%m%d_%H%M%S).md"
    local report_dir
    report_dir=$(dirname "$report_file")
    
    mkdir -p "$report_dir"
    
    local unfixed_issues=$((TOTAL_ISSUES - FIXED_ISSUES))
    
    local yaml_issues=0
    local ansible_issues=0
    
    if command -v rg >/dev/null 2>&1;
 then
        yaml_issues=$(rg -c -e "error|warning" /tmp/yamllint_output.txt 2>/dev/null || echo "0")
        ansible_issues=$(rg -c -e "error|warning" /tmp/ansible_lint_output.txt 2>/dev/null || echo "0")
    else
        yaml_issues=$(grep -E -c "error|warning" /tmp/yamllint_output.txt 2>/dev/null || echo "0")
        ansible_issues=$(grep -E -c "error|warning" /tmp/ansible_lint_output.txt 2>/dev/null || echo "0")
    fi

    local space_files=0
    local uppercase_count=0
    local fd_cmd=""
    if command -v fd >/dev/null 2>&1; then fd_cmd="fd"; elif command -v fdfind >/dev/null 2>&1; then fd_cmd="fdfind"; fi

    if [ -n "$fd_cmd" ]; then
        space_files=$("$fd_cmd" -g "* *" "$PROJECT_ROOT" --exclude .git | wc -l || echo "0")
        if [ -d "$PROJECT_ROOT/roles" ]; then
            uppercase_count=$("$fd_cmd" -t f -g "[A-Z]*" "$PROJECT_ROOT/roles" --exclude .git | wc -l || echo "0")
        fi
    else
        space_files=$(find "$PROJECT_ROOT" -name "* *" -not -path "*/.git/*" 2>/dev/null | wc -l || echo "0")
        if [ -d "$PROJECT_ROOT/roles" ]; then
            uppercase_count=$(find "$PROJECT_ROOT/roles" -type f -not -path "*/.git/*" 2>/dev/null | while read -r file;
 do
                base=$(basename "$file")
                [[ "$base" =~ ^[A-Z] ]] && echo "$file"
            done | wc -l || echo "0")
        fi
    fi
    
    local secret_files=0
    local unsafe_perm_files=0
    local secret_pattern='password\s*[:=]'
    local perm_pattern='mode:\s*['\''"]?(0?777|0?666)['\''"]?'

    if command -v rg >/dev/null 2>&1;
 then
        secret_files=$(rg -l -e "$secret_pattern" -g "*.yml" -g "*.yaml" --glob "!.git/*" "$PROJECT_ROOT" 2>/dev/null | wc -l || echo "0")
        unsafe_perm_files=$(rg -l -e "$perm_pattern" -g "*.yml" -g "*.yaml" --glob "!.git/*" "$PROJECT_ROOT" 2>/dev/null | wc -l || echo "0")
    else
        secret_files=$(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec grep -l -E "$secret_pattern" {} \; 2>/dev/null | wc -l || echo "0")
        unsafe_perm_files=$(find "$PROJECT_ROOT" \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/.git/*" -exec grep -l -E "$perm_pattern" {} \; 2>/dev/null | wc -l || echo "0")
    fi
    
    cat > "$report_file" << EOF
# Style Guide Compliance Report

**Generated:** $(date)
**Project:** Deploy-System-Unified

## Summary

- **Total Issues Found:** $TOTAL_ISSUES
- **Issues Auto-Fixed:** $FIXED_ISSUES
- **Issues Requiring Manual Attention:** $unfixed_issues

## Issues by Category

### YAML Formatting
$yaml_issues issues found

### Ansible Standards  
$ansible_issues issues found

### FQCN Compliance
$(command -v rg >/dev/null 2>&1 && rg -P -l '(?s)(-\s+name:.*?\n\s{2,}(?:apt|dnf|copy|template|service|systemd|shell|command|stat|mount|cron|assert|debug|set_fact|include_tasks|import_tasks|import_role|include_role):)|(^-\s+(?:apt|dnf|copy|template|service|systemd|shell|command|stat|mount|cron|assert|debug|set_fact|include_tasks|import_tasks|import_role|include_role):)' -g "roles/**/tasks/**/*.yml" -g "roles/**/tasks/*.yml" -g "roles/**/handlers/**/*.yml" -g "roles/**/handlers/*.yml" -g "roles/**/meta/**/*.yml" -g "roles/**/meta/*.yml" --glob "!.git/*" "$PROJECT_ROOT" 2>/dev/null | wc -l || echo "0") non-FQCN module calls found

### Shell Scripting
$(command -v shellcheck >/dev/null 2>&1 && find "$PROJECT_ROOT" -name "*.sh" -not -path "*/.git/*" -exec shellcheck {} + 2>/dev/null | grep -c "^In " || echo "0") issues found in standalone scripts

### Naming Conventions
$space_files files with spaces in names
$uppercase_count files with uppercase names in roles/

### Security Standards
$secret_files files with potential hardcoded secrets
$unsafe_perm_files files with potentially unsafe permissions

## Recommendations

1. Review and manually fix remaining issues
2. Run this tool regularly as part of development workflow
3. Consider integrating with pre-commit hooks
4. Refer to $STYLE_GUIDE for detailed style guidelines

## Tools Used

- yamllint: YAML linting
- ansible-lint: Ansible-specific linting
- shellcheck: Shell script linting
- ripgrep (rg) / grep: Pattern matching
- fd / find: File discovery
- awk/sed: Text processing

EOF

    success "Compliance report generated: $report_file"
}

# Script usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
  -h, --help             Show this help message
  -q, --quiet            Suppress output except errors
  -f, --fix              Auto-fix all fixable issues (including renames)
  -p, --low-risk-repair  Low-Risk Repair: Fix safe violations only (spaces, newlines)
  -r, --report           Generate compliance report only

Examples:
  $0                    # Run full style guide enforcement
  $0 --fix             # Auto-fix all issues
  $0 --low-risk-repair  # Run safe automatic repair tool
  $0 --report          # Generate compliance report only
EOF
}

# Main execution
main() {
    log "Starting style guide enforcement..."
    log "Project root: $PROJECT_ROOT"
    
    check_dependencies
    
    enforce_yaml_standards
    enforce_ansible_standards
    enforce_fqcn_standards
    enforce_shell_standards
    enforce_naming_conventions
    enforce_file_structure
    enforce_security_standards
    
    generate_report
    
    log "Style guide enforcement complete!"
    
    if [ $TOTAL_ISSUES -eq 0 ]; then
        success "✅ No style guide violations found!"
        exit 0
    else
        if [ "$REPORT_ONLY" = true ]; then
            warning "⚠️  Found $TOTAL_ISSUES style guide violations (Report Only Mode - Exiting Success)"
            exit 0
        fi
        warning "⚠️  Found $TOTAL_ISSUES style guide violations"
        warning "   $FIXED_ISSUES issues were auto-fixed"
        warning "   $((TOTAL_ISSUES - FIXED_ISSUES)) issues require manual attention"
        exit 1
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -q|--quiet)
            exec > /dev/null
            shift
            ;;
        -f|--fix)
            AUTO_FIX=true
            shift
            ;;
        -p|--low-risk-repair)
            LOW_RISK_REPAIR=true
            shift
            ;;
        -r|--report)
            REPORT_ONLY=true
            shift
            ;;
        *)
            error "Unknown option: $1"
            usage
            exit 1
            ;; 
    esac
done

# Run main function if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
