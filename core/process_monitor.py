import psutil

def monitor_processes(log_file):
    """Monitor running processes for suspicious activity."""
    suspicious_keywords = ["malware", "keylogger", "ransomware"]

    for process in psutil.process_iter(attrs=["pid", "name"]):
        try:
            process_name = process.info["name"]
            if any(keyword in process_name.lower() for keyword in suspicious_keywords):
                with open(log_file, "a") as log:
                    log.write(f"Suspicious process detected: {process_name} (PID: {process.info['pid']})\n")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue