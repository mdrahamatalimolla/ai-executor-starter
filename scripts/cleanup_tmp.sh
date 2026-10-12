#!/usr/bin/env bash
# উদাহরণ: tmp cleanup
set -euo pipefail
TARGET="${1:-/tmp}"
find "$TARGET" -type f -mtime +7 -delete
echo "Cleanup done on $TARGET"
