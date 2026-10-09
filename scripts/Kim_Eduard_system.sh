#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "$0")/.." && pwd)"

printf '%s\n' '==============================' 'Student Information' '==============================' ''
printf '%s\n' 'Name: Eduard' 'Surname: Kim' 'Group: IT2-2313' 'Student ID: 37324' ''
printf '%s\n' '==============================' 'System Information' '==============================' ''
printf 'Username: '; whoami
printf 'Hostname: '; hostname
printf 'Current Date: '; date
printf 'Operating System: '; uname -a
printf '\nDisk Usage:\n'; df -h
printf '\nMemory Usage:\n'; free -h
printf '\n'
if [[ -f "$project_dir/Kim_Eduard_info.txt" ]]; then
    echo 'Student information file exists.'
else
    echo 'Student information file does not exist.'
fi
