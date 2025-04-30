import os

def block_ip(ip_address):
    """Block an IP address."""
    os.system(f"iptables -A INPUT -s {ip_address} -j DROP")

def terminate_process(pid):
    """Terminate a process by PID."""
    try:
        os.kill(pid, 9)
    except Exception as e:
        print(f"Failed to terminate process {pid}: {e}")