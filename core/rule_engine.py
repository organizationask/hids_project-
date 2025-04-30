import re

def apply_rules(log_file, alert_file):
    """Apply rules to detect suspicious patterns in logs."""
    rules = [
        {"pattern": r"session opened", "message": "User session opened"},
        {"pattern": r"session closed", "message": "User session closed"},
        {"pattern": r"Authentication failure", "message": "Authentication failure detected"},
    ]

    with open(log_file, "r") as logs, open(alert_file, "a") as alerts:
        for line in logs:
            for rule in rules:
                if re.search(rule["pattern"], line):
                    alert_message = f"ALERT: {rule['message']} - {line.strip()}"
                    alerts.write(alert_message + "\n")
                    print(alert_message)