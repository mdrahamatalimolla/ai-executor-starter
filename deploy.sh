#!/usr/bin/env bash
# deploy.sh - build and run docker-compose for Si AI agent
set -euo pipefail
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$DIR"
if [ ! -f .env ]; then
  echo "API_KEY=REPLACE_WITH_STRONG_KEY" > .env
  echo "Created .env - edit and set a strong API_KEY before starting."
fi
sudo docker compose build --pull
sudo docker compose up -d
sudo docker compose ps
