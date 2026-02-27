#!/bin/sh
set -euo pipefail
# =================================================================================================
# SCRIPT: run_deployment_session.sh
# ARCHITECTURE: Agnostic (x86_64, aarch64, riscv64)
# OS SUPPORT: Linux, BSD, macOS (requires tmux)
# PURPOSE: Provides a resilient execution Environment for Ansible deployments using TMUX.
# =================================================================================================
#
# WHY THIS EXISTS:
#   Long-running Ansible playbooks are vulnerable to:
#   1. Network Disconnections (SSH pipe breaks -> Controller dies -> Deployment fails undefinedly)
#   2. Local Machine Sleep (Laptop lid closes -> Controller dies)
#   3. IDE/Terminal Crashes (VS Code window closes -> SIGHUP sent to Controller)
#
#   This script mitigates all of the above by decoupling the deployment process from your
#   current shell/IDE. It runs the playbook inside a detached TMUX session on the *Controller*
#   (this machine). If you disconnect, the session keeps running.
#
# INTEGRATION WITH CHECKPOINT SYSTEM:
#   This script is the perfect companion to the "Granular Checkpoint" system built into the
#   playbooks.
#   - Checkpoint System: Ensures if a role fails, we can resume.
#   - This Script: Ensures the deployment process doesn't die just because the UI died.
#
# USAGE:
#   ./scripts/run_deployment_session.sh [ansible-playbook-command]
#
# EXAMPLES:
#   1. Run a protected deployment:
#      ./scripts/run_deployment_session.sh ansible-playbook -i inventory/prod production_deploy.yml
#
#   2. Run with extra vars:
#      ./scripts/run_deployment_session.sh ansible-playbook base_hardened.yml -e "force_new_session=true"
#
# SESSION MANAGEMENT:
#   - To DETACH (keep running in background): Press 'Ctrl+b' then 'd'
#   - To REATTACH (resume viewing): Run this script again with no arguments, or use 'tmux attach -t deploy-session'
#
# =================================================================================================

SESSION_NAME="deploy-system-session"
LOG_FILE="./ansible_session.log"

# Function: Print usage
usage() {
    echo "Usage: $0 [command]"
    echo "  If a session exists: Attaches to the running deployment."
    echo "  If no session exists: Creates a new protected session and runs the command."
    echo ""
    echo "  Example: $0 ansible-playbook site.yml"
    exit 1
}

# 1. Dependency Check: Tmux (Cross-Platform)
if ! command -v tmux &> /dev/null; then
    echo "ERROR: 'tmux' is not installed."
    echo "This script requires tmux to provide session persistence."
    echo "Please install it using your system's package manager:"
    echo "  - Debian/Ubuntu: sudo apt install tmux"
    echo "  - RHEL-compatible (AlmaLinux/Rocky/CentOS Stream):   sudo dnf install tmux"
    echo "  - Arch Linux:    sudo pacman -S tmux"
    echo "  - Alpine:        sudo apk add tmux"
    echo "  - macOS:         brew install tmux"
    exit 1
fi


# 2. Context Check: Nested Tmux
if [ -n "$TMUX" ]; then
    echo "NOTICE: You are already inside a tmux session."
    echo "Executing command directly in current pane..."
    echo "---------------------------------------------------"
    "$@"
    exit $?
fi

# 3. Session Logic
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "==================================================="
    echo "   RESUMING EXISTING DEPLOYMENT SESSION"
    echo "==================================================="
    echo "A deployment session ('$SESSION_NAME') is already active."
    echo "Attaching you to the live output..."
    echo "(Press Ctrl+b, then d to detach again without stopping the deployment)"
    sleep 2
    tmux attach-session -t "$SESSION_NAME"
else
    # Verify arguments are provided for a new run
    if [ $# -eq 0 ]; then
        echo "No active session found and no command provided."
        usage
    fi

    echo "==================================================="
    echo "   STARTING NEW PROTECTED SESSION"
    echo "==================================================="
    echo "Command: $*"
    echo "Session: $SESSION_NAME"
    echo "Log:     $LOG_FILE"
    echo "---------------------------------------------------"
    echo "Initializing..."
    sleep 1
    
    # Create the session in detached mode
    # We pipe into tee so we have a raw log on disk as a secondary backup
    tmux new-session -d -s "$SESSION_NAME" "echo 'Started at $(date)'; $* | tee -a $LOG_FILE; echo '--------------------------------'; echo 'Process Finished. Press Enter to close session.'; read"
    
    # Configure the session to not die immediately if the command exits (allows reading final errors)
    tmux set-option -t "$SESSION_NAME" remain-on-exit off

    
    # Attach the user to the new session
    tmux attach-session -t "$SESSION_NAME"
fi
