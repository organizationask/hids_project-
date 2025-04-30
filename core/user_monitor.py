import os
import platform
import time
from datetime import datetime
import threading

def log_event(log_file, message):
    """Log an event to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:
        log.write(f"{timestamp} - {message}\n")

def monitor_users_linux(log_file):
    """Monitor user login/logout activity on Linux."""
    auth_log_path = "/var/log/auth.log"
    if not os.path.exists(auth_log_path):
        log_event(log_file, "Authentication log file not found.")
        return

    try:
        with open(auth_log_path, "r") as auth_log:
            auth_log.seek(0, os.SEEK_END)
            log_event(log_file, f"Monitoring user activity on: {auth_log_path}")
            while True:
                line = auth_log.readline()
                if not line:
                    time.sleep(1)
                    continue
                if "session opened" in line or "session closed" in line:
                    log_event(log_file, f"User activity: {line.strip()}")
    except Exception as e:
        log_event(log_file, f"Error monitoring users: {e}")

def monitor_users_windows(log_file):
    """Monitor user login/logout activity on Windows."""
    try:
        import wmi
        c = wmi.WMI()
        log_event(log_file, "Monitoring user activity on Windows Event Log.")
        watcher = c.Win32_NTLogEvent(EventCode="4624")  # EventCode 4624 is for logon events
        for event in watcher:
            log_event(log_file, f"User activity: {event.InsertionStrings}")
    except ImportError:
        log_event(log_file, "The 'wmi' module is required for Windows user monitoring.")
    except Exception as e:
        log_event(log_file, f"Error monitoring users: {e}")

def monitor_users(log_file):
    """Monitor user login/logout activity based on the platform."""
    if platform.system() == "Linux":
        monitor_users_linux(log_file)
    elif platform.system() == "Windows":
        monitor_users_windows(log_file)
    else:
        log_event(log_file, "User monitoring is not supported on this platform.")

if __name__ == "__main__":
    LOG_FILE = "logs/intrusion_logs.txt"

    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Start monitoring users
    threading.Thread(target=monitor_users, args=(LOG_FILE,), daemon=True).start()