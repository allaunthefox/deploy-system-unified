#!/bin/bash
# CI Canary Script - Intentionally Bad Shell Script
# This file contains common shellcheck violations

# SC2086: Double quote to prevent globbing and word splitting
echo $UNQUOTED_VARIABLE

# SC2006: Use $(...) notation instead of legacy backticks
FILES=`ls -la`

# SC2046: Quote this to prevent word splitting
cp $(cat files.txt) /destination/

# SC2034: Unused variables
UNUSED_VAR="this is never used"

# SC2068: Double quote array expansions
array=(one two three)
for item in ${array[@]}; do
    echo $item
done

# Fake credentials in shell script
HARDCODED_PASSWORD="SuperSecret123!"
DB_PASSWORD=s3cr3tP@ssw0rd
API_KEY="sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
