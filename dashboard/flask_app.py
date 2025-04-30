from flask import Flask, render_template, jsonify
try:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hids')))
    from data_collector import attack_logs, start_real_time_monitoring
except ImportError:
    raise ImportError("The module 'hids.data_collector' could not be resolved. Ensure it is installed and accessible.")
import threading

app = Flask(__name__)

@app.route("/")
def index():
    """Render the dashboard."""
    return render_template("index.html")

@app.route("/logs")
def get_logs():
    """Return the latest logs."""
    return jsonify({"logs": attack_logs})

def start_monitoring():
    """Start real-time monitoring in a separate thread."""
    monitoring_thread = threading.Thread(target=start_real_time_monitoring, daemon=True)
    monitoring_thread.start()

if __name__ == "__main__":
    start_monitoring()
    app.run(debug=True)