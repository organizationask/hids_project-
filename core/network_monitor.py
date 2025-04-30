from scapy.all import sniff, IP, TCP, UDP, ICMP
import time
from core.alert_manager import send_email_alert

def log_event(log_file, message):
    """Log an event to the log file."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:
        log.write(f"{timestamp} - {message}\n")

def punish_user(ip_address, log_file):
    """Take action against a specific IP address."""
    message = f"Punishment triggered for IP: {ip_address} due to suspicious activity."
    log_event(log_file, message)
    print(message)
    # Send an email alert
    send_email_alert(
        subject="Suspicious Activity Detected",
        message=message,
        to_email="admin@example.com"  # Replace with the admin's email address
    )

def monitor_network_traffic(log_file, interface=None, target_ip=None):
    """
    Monitor network traffic in real-time and log activity for a specific host IP.

    Args:
        log_file (str): The file to log detected events.
        interface (str): The network interface to monitor.
        target_ip (str): The specific IP address to monitor. If None, log all traffic.
    """
    def process_packet(packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst

            # Filter packets based on the target IP
            if target_ip and target_ip not in [src_ip, dst_ip]:
                return

            # Log TCP traffic
            if TCP in packet:
                log_event(log_file, f"TCP Packet: {src_ip} -> {dst_ip} (Port: {packet[TCP].dport})")

            # Log UDP traffic
            elif UDP in packet:
                log_event(log_file, f"UDP Packet: {src_ip} -> {dst_ip} (Port: {packet[UDP].dport})")

            # Log ICMP traffic
            elif ICMP in packet:
                log_event(log_file, f"ICMP Packet: {src_ip} -> {dst_ip}")

            # Log other IP traffic
            else:
                log_event(log_file, f"IP Packet: {src_ip} -> {dst_ip}")

            # Trigger punishment for suspicious activity
            if target_ip and (src_ip == target_ip or dst_ip == target_ip):
                punish_user(target_ip, log_file)

    print(f"Starting network monitoring on interface: {interface} for target IP: {target_ip}")
    sniff(iface=interface, prn=process_packet, store=False)