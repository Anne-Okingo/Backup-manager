#!/usr/bin/env python3
import os
import time
import tarfile
from datetime import datetime

def log_message(message):
    """Write a timestamped message to the backup_service.log file"""
    timestamp = datetime.now().strftime("[%d/%m/%Y %H:%M]")
    log_entry = f"{timestamp} {message}\n"
    
    os.makedirs("logs", exist_ok=True)
    with open("logs/backup_service.log", "a") as log_file:
        log_file.write(log_entry)

def create_backup(source_path, backup_name):
    """Create a tar backup of the source path"""
    os.makedirs("backups", exist_ok=True)
    backup_path = f"backups/{backup_name}.tar"
    
    try:
        with tarfile.open(backup_path, "w") as tar:
            tar.add(source_path, arcname=os.path.basename(source_path))
        log_message(f"Backup done for {source_path} in {backup_path}")
        return True
    except Exception as e:
        log_message(f"Error creating backup for {source_path}: {str(e)}")
        return False

def check_schedules():
    """Check schedules and perform backups if time matches"""
    current_time = datetime.now().strftime("%H:%M")
    
    try:
        with open("backup_schedules.txt", "r") as f:
            schedules = f.readlines()
        
        for schedule in schedules:
            schedule = schedule.strip()
            if not schedule:
                continue
                
            parts = schedule.split(';')
            if len(parts) != 3:
                continue
                
            source_path, scheduled_time, backup_name = parts
            
            if scheduled_time == current_time:
                create_backup(source_path, backup_name)
                
    except FileNotFoundError:
        pass  # No schedules file yet

def main():
    """Main service loop"""
    log_message("backup_service started")
    
    while True:
        check_schedules()
        time.sleep(45)  # Sleep for 45 seconds

if __name__ == "__main__":
    main()