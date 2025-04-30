from flask import Flask, render_template, jsonify, request
import threading
from core.user_monitor import monitor_users
from core.file_monitor import monitor_files
from core.rule_engine import apply_rules

app = Flask(__name__)

# Global variable to store the target IP
target_ip = None

@app.route("/")
def index():
    """Render the dashboard."""
    return render_template("index.html")

@app.route("/logs")
def get_logs():
    """Return the latest logs."""
    log_file = "logs/intrusion_logs.txt"
    try:
        with open(log_file, "r") as log:
            logs = log.readlines()
        return jsonify({"logs": logs})
    except FileNotFoundError:
        return jsonify({"logs": []})

@app.route("/alerts")
def get_alerts():
    """Return the latest alerts."""
    alert_file = "logs/alerts.txt"
    try:
        with open(alert_file, "r") as alerts:
            alert_logs = alerts.readlines()
            # Filter out any port-related alerts (if any exist)
            filtered_alerts = [alert for alert in alert_logs if "port" not in alert.lower()]
        return jsonify({"alerts": filtered_alerts})
    except FileNotFoundError:
        return jsonify({"alerts": []})

@app.route("/set_target_ip", methods=["POST"])
def set_target_ip():
    """Set the target IP address for monitoring."""
    global target_ip
    target_ip = request.json.get("target_ip")
    if target_ip:
        return jsonify({"message": f"Target IP set to {target_ip}"}), 200
    return jsonify({"error": "Invalid IP address"}), 400

@app.route("/host_logs")
def get_host_logs():
    """Return logs filtered by the target IP."""
    global target_ip
    if not target_ip:
        return jsonify({"logs": []})
    log_file = "logs/intrusion_logs.txt"
    try:
        with open(log_file, "r") as log:
            logs = log.readlines()
            filtered_logs = [log for log in logs if target_ip in log]
        return jsonify({"logs": filtered_logs})
    except FileNotFoundError:
        return jsonify({"logs": []})

@app.route("/host_alerts")
def get_host_alerts():
    """Return alerts filtered by the target IP."""
    global target_ip
    if not target_ip:
        return jsonify({"alerts": []})
    alert_file = "logs/alerts.txt"
    try:
        with open(alert_file, "r") as alerts:
            alert_logs = alerts.readlines()
            filtered_alerts = [alert for alert in alert_logs if target_ip in alert and "port" not in alert.lower()]
        return jsonify({"alerts": filtered_alerts})
    except FileNotFoundError:
        return jsonify({"alerts": []})

def start_user_monitoring():
    """Start user activity monitoring."""
    monitor_users("logs/intrusion_logs.txt")

def start_file_monitoring():
    """Start file integrity monitoring."""
    monitor_files("C:\\path\\to\\directory", "logs/intrusion_logs.txt")

def start_rule_engine():
    """Start the rule engine."""
    apply_rules("logs/intrusion_logs.txt", "logs/alerts.txt")

if __name__ == "__main__":
    # Display "AKASH" in a stylish format
    print("""
     █████╗ ██╗  ██╗ █████╗ ███████╗██╗  ██╗
    ██╔══██╗██║ ██╔╝██╔══██╗██╔════╝██║ ██╔╝
    ███████║█████╔╝ ███████║███████╗█████╔╝ 
    ██╔══██║██╔═██╗ ██╔══██║╚════██║██╔═██╗ 
    ██║  ██║██║  ██╗██║  ██║███████║██║  ██╗
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """)

    # Display "Created by Akash Patil" in the terminal
    print("===================================")
    print("       Created by Akash Patil      ")
    print("===================================")

    # Ensure the logs directory exists
    import os
    os.makedirs("logs", exist_ok=True)

    # Start monitoring in separate threads
    threading.Thread(target=start_user_monitoring, daemon=True).start()
    threading.Thread(target=start_file_monitoring, daemon=True).start()
    threading.Thread(target=start_rule_engine, daemon=True).start()

    # Start the Flask app
    app.run(debug=True)