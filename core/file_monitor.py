import os
import hashlib
import time

def monitor_files(directory, log_file, interval=5):
    """
    Monitor changes in a directory for unauthorized modifications, additions, and deletions.

    Args:
        directory (str): The directory to monitor.
        log_file (str): The file to log detected events.
        interval (int): The polling interval in seconds.
    """
    file_hashes = {}

    print(f"Starting file monitoring on directory: {directory}")
    while True:
        current_files = {}
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Calculate the hash of the file
                    with open(file_path, "rb") as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    current_files[file_path] = file_hash

                    # Check for new or modified files
                    if file_path not in file_hashes:
                        log_event(log_file, f"New file detected: {file_path}")
                    elif file_hashes[file_path] != file_hash:
                        log_event(log_file, f"File modified: {file_path}")
                except Exception as e:
                    log_event(log_file, f"Error reading file {file_path}: {e}")

        # Check for deleted files
        deleted_files = set(file_hashes.keys()) - set(current_files.keys())
        for deleted_file in deleted_files:
            log_event(log_file, f"File deleted: {deleted_file}")

        # Update the file hashes
        file_hashes = current_files

        # Wait for the next polling interval
        time.sleep(interval)

def log_event(log_file, message):
    """
    Log an event to the log file.

    Args:
        log_file (str): The file to log the event.
        message (str): The message to log.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)  # Print to console for debugging
    with open(log_file, "a") as log:
        log.write(log_entry + "\n")

if __name__ == "__main__":
    DIRECTORY_TO_MONITOR = "C:\\path\\to\\directory"  # Replace with the directory you want to monitor
    LOG_FILE = "C:\\path\\to\\logs\\file_monitor_logs.txt"  # Replace with the path to your log file

    try:
        monitor_files(DIRECTORY_TO_MONITOR, LOG_FILE)
    except KeyboardInterrupt:
        print("File monitoring stopped.")