import os
import psutil
import shutil
import time
import smtplib
from collections import defaultdict
from email.mime.text import MIMEText

QUARANTINE_DIR = "/var/quarantine"
command_threshold = 10  # Example threshold
user_command_count = defaultdict(int)

# Ensure the quarantine directory exists
os.makedirs(QUARANTINE_DIR, exist_ok=True)

def monitor_processes():
    processes = {}
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time', 'cmdline']):
            if proc.info['pid'] not in processes:
                processes[proc.info['pid']] = proc.info
                print(f"New Process Detected: {proc.info}")
                analyze_user_behavior(proc.info)
        time.sleep(1)

def analyze_user_behavior(process_info):
    user_command_count[process_info['username']] += 1
    if user_command_count[process_info['username']] > command_threshold:
        print(f"Potential Threat Detected: User {process_info['username']} has executed {user_command_count[process_info['username']]} commands in a short period.")
        send_alert(process_info['username'], user_command_count[process_info['username']])
        quarantine_process(process_info)

def quarantine_process(proc_info):
    try:
        proc = psutil.Process(proc_info['pid'])
        proc.terminate()

        exe_path = proc_info['cmdline'][0] if proc_info['cmdline'] else None
        if exe_path and os.path.isfile(exe_path):
            quarantine_path = os.path.join(QUARANTINE_DIR, os.path.basename(exe_path))
            shutil.move(exe_path, quarantine_path)
            print(f"Process {proc_info['name']} (PID {proc_info['pid']}) terminated and executable moved to quarantine.")
        else:
            print(f"Process {proc_info['name']} (PID {proc_info['pid']}) terminated, but no executable found for quarantine.")
    except Exception as e:
        print(f"Failed to quarantine process {proc_info['name']} (PID {proc_info['pid']}): {e}")

def send_alert(user, command_count):
    msg = MIMEText(f"Alert: User {user} has executed {command_count} commands in a short period.")
    msg['Subject'] = 'EDR Threat Alert'
    msg['From'] = 'edr-system@example.com'
    msg['To'] = 'admin@example.com'

    try:
        with smtplib.SMTP('localhost') as server:
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
    except Exception as e:
        print(f"Failed to send alert email: {e}")

if __name__ == "__main__":
    monitor_processes()
