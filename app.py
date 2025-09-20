from flask import Flask, request, jsonify
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

app = Flask(__name__)

# ---- logging setup (absolute path + INFO level) ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "access.log")

handler = RotatingFileHandler(LOG_PATH, maxBytes=5*1024*1024, backupCount=2)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(message)s'))

app.logger.setLevel(logging.INFO)   # <-- critical, ensures INFO is written
app.logger.addHandler(handler)

def log_access(status=200):
    """Write a combined-style access log line."""
    ip = request.remote_addr or "-"
    now = datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S +0000")
    method = request.method
    path = request.path + (("?" + request.query_string.decode()) if request.query_string else "")
    line = f'{ip} - - [{now}] "{method} {path}" {status}'
    app.logger.info(line)

# ---- demo data ----
USERS = {"alice": "password123", "bob": "hunter2"}

@app.route("/")
def index():
    log_access(200)
    return "Demo app running\n"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        log_access(200)
        return """<form method="post">
                    <input name="username" placeholder="username"/>
                    <input name="password" type="password" placeholder="password"/>
                    <button>Login</button>
                  </form>"""
    # POST = check login
    username = request.form.get("username")
    password = request.form.get("password")
    if USERS.get(username) == password:
        log_access(200)
        return jsonify({"ok": True, "msg": "welcome"})
    else:
        log_access(401)
        return jsonify({"ok": False, "msg": "invalid"}), 401

@app.route("/search")
def search():
    q = request.args.get("q", "")
    log_access(200)
    return jsonify({"query": q, "hits": []})

if __name__ == "__main__":
    # change HOST to 127.0.0.1 if you want local-only access
    # allow PORT and HOST to be configured via environment for cloud deployments
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    app.run(host=host, port=port, debug=debug)

