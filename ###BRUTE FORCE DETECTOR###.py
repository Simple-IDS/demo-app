###BRUTE FORCE DETECTOR###
import re
from collections import defaultdict
from datetime import datetime, timedelta
import time

log_file = 'access.log'
time_window = timedelta(minutes=5)  
threshold = 30      
failed_attempts = defaultdict(list)

def parse_log_line(line):
    match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+- - \[(.*?)\]\s+"(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)\s+(.*?)"\s+(\d+)',
        line)
    if match:
        timestamp_str, ip_address = match.groups()
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        return timestamp, ip_address
    return None, None

def detect_brute_force(log_file):
    with open(log_file, 'r') as f:
        for line in f:
            timestamp, ip = parse_log_line(line)
            if not ip:
                continue
            current_time = datetime.now()
            ip_attempts = failed_attempts[ip]
            ip_attempts = [t for t in ip_attempts if current_time - t < time_window]
            ip_attempts.append(timestamp)
            failed_attempts[ip] = ip_attempts
            if len(ip_attempts) > threshold:
                print(f"{style.RED}Brute-force attack detected from IP: {ip}{style.RESET}")
                failed_attempts[ip] = []
def periodically():
    print("Starting a new cycle...")
    detect_brute_force(log_file)
    print("Cycle complete. Waiting for the next interval...")

if __name__ == "__main__":
    print("Monitoring logs for brute-force activity...")
    detect_brute_force(log_file)
    time.sleep(300)