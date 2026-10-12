#!/usr/bin/env bash
# উদাহরণ: ব্যাকআপ স্ক্রিপ্ট — কাস্টমাইজ করুন
set -euo pipefail
DST="/opt/executor/backups"
mkdir -p "$DST"
tar -czf "$DST/backup-$(date +%Y%m%d-%H%M%S).tar.gz" /home/$USER/somefolder || true
echo "Backup completed to $DST"
