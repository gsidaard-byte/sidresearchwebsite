#!/bin/zsh

set -euo pipefail

repo_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$repo_dir"

timestamp="$(date +"%Y-%m-%d %H:%M")"
message="${1:-Snapshot ${timestamp}}"

git add -A

if git diff --cached --quiet; then
  echo "No changes to snapshot."
  exit 0
fi

git commit -m "$message"
echo "Created snapshot commit: $message"
