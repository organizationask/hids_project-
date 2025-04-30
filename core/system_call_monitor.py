import os

def monitor_system_calls(log_file):
    """Monitor system calls for anomalies."""
    try:
        with open("/proc/syscalls", "r") as syscalls:
            for line in syscalls:
                if "unauthorized" in line or "denied" in line:
                    with open(log_file, "a") as log:
                        log.write(f"System call anomaly detected: {line}")
    except FileNotFoundError:
        with open(log_file, "a") as log:
            log.write("System call monitoring not supported on this system.\n")