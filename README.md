# Si AI agent — Approval UI and deployment

## New files added
- `ui/` — static approval UI (open http://localhost:8000 when docker-compose is running)
- `deploy.sh` — helper script to build and run docker-compose
- `systemd/si-executor.service` — example systemd unit
- `.env.template` — env file template

## How to run (quick)
1. Copy repository to server and prepare scripts

```bash
sudo mkdir -p /opt/executor
sudo chown $USER:$USER /opt/executor
cp -r scripts /opt/executor/
chmod +x /opt/executor/scripts/*.sh
```

2. Edit `.env` (or copy `.env.template`) and set a strong API_KEY

```bash
cp .env.template .env
# then edit .env -> API_KEY=your_strong_key_here
```

3. Build & run

```bash
chmod +x deploy.sh
./deploy.sh
```

4. Access UI
- Approval UI: http://localhost:8000
- Executor API (local): http://localhost:5000

5. Test flow
- From any chat UI (or curl) create a proposal:
```
curl -X POST -H "Content-Type: application/json" \
  -d '{"command":"cleanup_tmp","args":["/tmp/testdir"],"note":"clean old tmp"}' \
  http://127.0.0.1:5000/propose
```
- Open Approval UI: http://localhost:8000 — enter API_KEY, Refresh, Approve/Reject

Security reminders
- Keep services bound to localhost; do not expose publicly without TLS+auth.
- Keep `whitelist.json` minimal and use absolute paths only.
- Use Docker resource limits and run executor as non-root (Dockerfile does this).
