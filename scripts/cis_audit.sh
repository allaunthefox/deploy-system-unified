#!/bin/bash
#
# CIS Benchmark Audit Script
# Validates system configuration against CIS Ubuntu Linux 22.04 LTS Benchmark
#
# Usage: ./cis_audit.sh [--level 1|2] [--report] [--json]
#

set -e

# Configuration
CIS_LEVEL="${CIS_LEVEL:-1}"
REPORT_PATH="${REPORT_PATH:-/var/lib/deploy-system/compliance}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0
TOTAL_COUNT=0

# Functions
log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASS_COUNT++))
    ((TOTAL_COUNT++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAIL_COUNT++))
    ((TOTAL_COUNT++))
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    ((WARN_COUNT++))
    ((TOTAL_COUNT++))
}

check_file_permissions() {
    local file="$1"
    local expected_mode="$2"
    
    if [ ! -f "$file" ]; then
        log_warn "$file does not exist"
        return
    fi
    
    local actual_mode=$(stat -c '%a' "$file" 2>/dev/null)
    if [ "$actual_mode" == "$expected_mode" ]; then
        log_pass "$file has correct permissions ($expected_mode)"
    else
        log_fail "$file has incorrect permissions ($actual_mode, expected $expected_mode)"
    fi
}

check_sysctl() {
    local param="$1"
    local expected="$2"
    
    local actual=$(sysctl -n "$param" 2>/dev/null || echo "N/A")
    if [ "$actual" == "$expected" ]; then
        log_pass "$param = $actual"
    else
        log_fail "$param = $actual (expected $expected)"
    fi
}

check_service() {
    local service="$1"
    local expected_state="$2"
    
    local state=$(systemctl is-active "$service" 2>/dev/null || echo "inactive")
    if [ "$state" == "$expected_state" ]; then
        log_pass "$service is $expected_state"
    else
        log_fail "$service is $state (expected $expected_state)"
    fi
}

check_package() {
    local package="$1"
    local should_exist="$2"
    
    if dpkg -l "$package" &>/dev/null || rpm -q "$package" &>/dev/null; then
        if [ "$should_exist" == "true" ]; then
            log_pass "$package is installed"
        else
            log_fail "$package is installed (should be removed)"
        fi
    else
        if [ "$should_exist" == "false" ]; then
            log_pass "$package is not installed"
        else
            log_fail "$package is not installed"
        fi
    fi
}

# Main Audit Functions
audit_filesystem() {
    echo ""
    echo "=== Filesystem Security (CIS 1.x) ==="
    
    # CIS 1.1.1 - Ensure mounting of squashfs filesystems is disabled
    if modprobe -n -v squashfs 2>&1 | grep -q "install /bin/true"; then
        log_pass "CIS 1.1.1: squashfs mounting is disabled"
    else
        log_fail "CIS 1.1.1: squashfs mounting is not disabled"
    fi
    
    # CIS 1.1.2 - Ensure mounting of udf filesystems is disabled
    if modprobe -n -v udf 2>&1 | grep -q "install /bin/true"; then
        log_pass "CIS 1.1.2: udf mounting is disabled"
    else
        log_fail "CIS 1.1.2: udf mounting is not disabled"
    fi
    
    # CIS 1.2.2 - Ensure nodev option set on /tmp partition
    if mount | grep " /tmp " | grep -q "nodev"; then
        log_pass "CIS 1.2.2: nodev is set on /tmp"
    else
        log_warn "CIS 1.2.2: nodev is not set on /tmp"
    fi
    
    # CIS 1.2.5 - Ensure /dev/shm is a separate partition
    if mount | grep -q "shm tmpfs"; then
        log_pass "CIS 1.2.5: /dev/shm is mounted"
    else
        log_warn "CIS 1.2.5: /dev/shm is not a separate partition"
    fi
}

audit_network() {
    echo ""
    echo "=== Network Configuration (CIS 3.x) ==="
    
    # CIS 3.1.1 - Ensure IP forwarding is disabled
    check_sysctl "net.ipv4.ip_forward" "0"
    
    # CIS 3.1.2 - Ensure packet redirect sending is disabled
    check_sysctl "net.ipv4.conf.all.send_redirects" "0"
    
    # CIS 3.2.1 - Ensure ICMP redirects are not accepted
    check_sysctl "net.ipv4.conf.all.accept_redirects" "0"
    
    # CIS 3.2.2 - Ensure secure ICMP redirects are not accepted
    check_sysctl "net.ipv4.conf.all.secure_redirects" "0"
    
    # CIS 3.2.3 - Ensure suspicious packet responses are logged
    check_sysctl "net.ipv4.conf.all.log_martians" "1"
    
    # CIS 3.2.4 - Ensure broadcast ICMP requests are ignored
    check_sysctl "net.ipv4.icmp_echo_ignore_broadcasts" "1"
    
    # CIS 3.2.7 - Ensure TCP SYN Cookies is enabled
    check_sysctl "net.ipv4.tcp_syncookies" "1"
    
    # CIS 3.2.8 - Ensure Reverse Path Filtering is enabled
    check_sysctl "net.ipv4.conf.all.rp_filter" "1"
}

audit_logging() {
    echo ""
    echo "=== Logging and Auditing (CIS 4.x) ==="
    
    # CIS 4.1.1 - Ensure auditd is installed
    check_package "auditd" "true"
    
    # CIS 4.1.2 - Ensure auditd service is enabled
    if systemctl is-enabled auditd &>/dev/null; then
        log_pass "CIS 4.1.2: auditd is enabled"
    else
        log_fail "CIS 4.1.2: auditd is not enabled"
    fi
    
    # CIS 4.2.1 - Ensure auditing for processes prior to auditd is enabled
    if grep -q "audit=1" /proc/cmdline 2>/dev/null; then
        log_pass "CIS 4.2.1: audit=1 is set in kernel parameters"
    else
        log_warn "CIS 4.2.1: audit=1 is not set in kernel parameters"
    fi
}

audit_access_control() {
    echo ""
    echo "=== Access Control (CIS 5.x) ==="
    
    # CIS 5.1.1 - Ensure permissions on /etc/shadow are configured
    check_file_permissions "/etc/shadow" "640"
    
    # CIS 5.1.2 - Ensure permissions on /etc/passwd are configured
    check_file_permissions "/etc/passwd" "644"
    
    # CIS 5.5.9 - Ensure SSH root login is disabled
    if sshd -T 2>/dev/null | grep -q "^permitrootlogin no" || \
       grep -q "^PermitRootLogin no" /etc/ssh/sshd_config 2>/dev/null; then
        log_pass "CIS 5.5.9: SSH root login is disabled"
    else
        log_fail "CIS 5.5.9: SSH root login is not disabled"
    fi
    
    # CIS 5.5.10 - Ensure SSH PermitEmptyPasswords is disabled
    if sshd -T 2>/dev/null | grep -q "^permitemptypasswords no" || \
       grep -q "^PermitEmptyPasswords no" /etc/ssh/sshd_config 2>/dev/null; then
        log_pass "CIS 5.5.10: SSH empty passwords are disabled"
    else
        log_fail "CIS 5.5.10: SSH empty passwords are not disabled"
    fi
    
    # CIS 5.5.5 - Ensure SSH MaxAuthTries is set to 4 or less
    local max_auth=$(sshd -T 2>/dev/null | grep "^maxauthtries" | awk '{print $2}' || \
                    grep "^MaxAuthTries" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}' || echo "6")
    if [ "$max_auth" -le 4 ] 2>/dev/null; then
        log_pass "CIS 5.5.5: SSH MaxAuthTries is $max_auth"
    else
        log_fail "CIS 5.5.5: SSH MaxAuthTries is $max_auth (should be <= 4)"
    fi
}

audit_mac() {
    echo ""
    echo "=== Mandatory Access Control (CIS 9.x) ==="
    
    # CIS 9.1.1 - Ensure AppArmor is installed
    check_package "apparmor" "true"
    
    # CIS 9.1.2 - Ensure AppArmor is enabled in bootloader
    if grep -q "apparmor=1" /proc/cmdline 2>/dev/null; then
        log_pass "CIS 9.1.2: AppArmor is enabled in bootloader"
    else
        log_warn "CIS 9.1.2: AppArmor may not be enabled in bootloader"
    fi
}

print_summary() {
    echo ""
    echo "========================================"
    echo "           CIS Audit Summary"
    echo "========================================"
    echo -e "Total Checks:  $TOTAL_COUNT"
    echo -e "${GREEN}Passed:${NC}       $PASS_COUNT"
    echo -e "${RED}Failed:${NC}       $FAIL_COUNT"
    echo -e "${YELLOW}Warnings:${NC}     $WARN_COUNT"
    
    if [ $TOTAL_COUNT -gt 0 ]; then
        local percentage=$((PASS_COUNT * 100 / TOTAL_COUNT))
        echo ""
        echo -e "Compliance Score: ${GREEN}${percentage}%${NC}"
        
        if [ $percentage -ge 95 ]; then
            echo -e "Status: ${GREEN}PASS${NC} (CIS Level 1)"
        elif [ $percentage -ge 80 ]; then
            echo -e "Status: ${YELLOW}PARTIAL${NC} (Improvement needed)"
        else
            echo -e "Status: ${RED}FAIL${NC} (Significant gaps)"
        fi
    fi
    echo "========================================"
}

generate_report() {
    mkdir -p "$REPORT_PATH"
    local report_file="$REPORT_PATH/cis_audit_$(date +%Y%m%d_%H%M%S).json"
    
    cat > "$report_file" << EOF
{
  "audit_timestamp": "$(date -Iseconds)",
  "hostname": "$(hostname)",
  "cis_level": "$CIS_LEVEL",
  "summary": {
    "total": $TOTAL_COUNT,
    "passed": $PASS_COUNT,
    "failed": $FAIL_COUNT,
    "warnings": $WARN_COUNT,
    "compliance_percentage": $((PASS_COUNT * 100 / TOTAL_COUNT))
  }
}
EOF
    
    echo ""
    echo "Report saved to: $report_file"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --level)
            CIS_LEVEL="$2"
            shift 2
            ;;
        --report)
            GENERATE_REPORT="true"
            shift
            ;;
        --json)
            OUTPUT_FORMAT="json"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--level 1|2] [--report] [--json]"
            echo ""
            echo "Options:"
            echo "  --level 1|2    CIS Benchmark level (default: 1)"
            echo "  --report       Generate JSON report"
            echo "  --json         Output in JSON format"
            echo "  -h, --help     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Main execution
echo "========================================"
echo "    CIS Benchmark Audit Script"
echo "    Level: $CIS_LEVEL"
echo "    Date: $(date)"
echo "========================================"

audit_filesystem
audit_network
audit_logging
audit_access_control

if [ "$CIS_LEVEL" == "2" ]; then
    audit_mac
fi

print_summary

if [ "$GENERATE_REPORT" == "true" ]; then
    generate_report
fi

# Exit with appropriate code
if [ $FAIL_COUNT -gt 0 ]; then
    exit 1
fi
exit 0
