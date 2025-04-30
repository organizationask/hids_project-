from scapy.all import sniff, IP, TCP
from datetime import datetime

# Global variables to track attack logs
attack_logs = []

def log_event(event_type, details):
    """Log an event with its type and details."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"{timestamp} - {event_type}: {details}"
    print(log)
    attack_logs.append(log)

def monitor_traffic(packet):
    """Monitor network traffic and log suspicious activity."""
    if IP in packet:
        if TCP in packet:
            # Example: Detect traffic on port 22 (SSH)
            if packet[TCP].dport == 22:
                log_event("Suspicious Traffic", f"SSH traffic detected from {packet[IP].src} to {packet[IP].dst}")
            # Example: Detect traffic on port 80 (HTTP)
            elif packet[TCP].dport == 80:
                log_event("Suspicious Traffic", f"HTTP traffic detected from {packet[IP].src} to {packet[IP].dst}")
            # Add more rules for detecting malicious activity
            else:
                log_event("Traffic", f"Traffic detected from {packet[IP].src} to {packet[IP].dst} on port {packet[TCP].dport}")

def start_real_time_monitoring(monitored_ip=None):
    """Start real-time monitoring of all 65,535 ports."""
    filter_rule = f"host {monitored_ip}" if monitored_ip else "ip"
    print(f"Starting real-time monitoring with filter: {filter_rule}")
    sniff(filter=filter_rule, prn=monitor_traffic, store=0)