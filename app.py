from flask import Flask, request, jsonify, abort
import os
import json
import sqlite3
import subprocess
from datetime import datetime

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(APP_DIR, "proposals.db")
WHITELIST_PATH = os.path.join(APP_DIR, "whitelist.json")
API_KEY = os.environ.get("API_KEY", "please-set-a-strong-key")

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS proposals (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      command_key TEXT NOT NULL,
      args TEXT,
      note TEXT,
      status TEXT NOT NULL,
      created_at TEXT,
      executed_at TEXT,
      return_code INTEGER,
      output TEXT
    )
    """)
    conn.commit()
    conn.close()

def load_whitelist():
    with open(WHITELIST_PATH, "r") as f:
        return json.load(f)

@app.route("/propose", methods=["POST"])
def propose():
    data = request.get_json(force=True)
    command_key = data.get("command")
    args = data.get("args", [])
    note = data.get("note", "")
    if not command_key:
        return jsonify({"error": "missing command key"}), 400
    wl = load_whitelist()
    if command_key not in wl:
        return jsonify({"error": "command not in whitelist"}), 400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO proposals (command_key, args, note, status, created_at) VALUES (?, ?, ?, 'pending', ?)",
              (command_key, json.dumps(args), note, datetime.utcnow().isoformat()))
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"id": pid, "status": "pending"}), 201

@app.route("/proposals", methods=["GET"])
def list_proposals():
    state = request.args.get("state")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if state:
        c.execute("SELECT * FROM proposals WHERE status=? ORDER BY id DESC", (state,))
    else:
        c.execute("SELECT * FROM proposals ORDER BY id DESC")
    rows = c.fetchall()
    cols = [d[0] for d in c.description]
    res = []
    for r in rows:
        res.append(dict(zip(cols, r)))
    conn.close()
    return jsonify(res)

def check_api_key(req):
    key = req.headers.get("X-API-KEY") or req.args.get("api_key")
    return key == API_KEY

@app.route("/approve/<int:pid>", methods=["POST"])
def approve(pid):
    if not check_api_key(request):
        abort(401)
    data = request.get_json(force=True)
    do_approve = data.get("approve", True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT command_key, args, status FROM proposals WHERE id=?", (pid,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "not found"}), 404
    command_key, args_json, status = row
    if status != "pending":
        conn.close()
        return jsonify({"error": "proposal not pending", "status": status}), 400
    if not do_approve:
        c.execute("UPDATE proposals SET status='rejected' WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        return jsonify({"id": pid, "status": "rejected"})
    wl = load_whitelist()
    cmd_info = wl.get(command_key)
    if not cmd_info:
        conn.close()
        return jsonify({"error": "whitelist changed, command missing"}), 500
    try:
        args = json.loads(args_json) if args_json else []
    except:
        args = []
    exec_cmd = [cmd_info["path"]] + args
    c.execute("UPDATE proposals SET status='approved' WHERE id=?", (pid,))
    conn.commit()
    try:
        proc = subprocess.run(exec_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300, text=True)
        output = proc.stdout
        rc = proc.returncode
        new_status = "done" if rc == 0 else "failed"
    except subprocess.TimeoutExpired as e:
        output = f"Timeout: {str(e)}"
        rc = -1
        new_status = "failed"
    except Exception as e:
        output = f"Error running command: {str(e)}"
        rc = -2
        new_status = "failed"
    executed_at = datetime.utcnow().isoformat()
    c.execute("UPDATE proposals SET status=?, executed_at=?, return_code=?, output=? WHERE id=?",
              (new_status, executed_at, rc, output, pid))
    conn.commit()
    conn.close()
    return jsonify({"id": pid, "status": new_status, "return_code": rc, "output": output})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
