#!/usr/bin/env python3
import sys
import os
from datetime import datetime

def log_message(message):
    """Write a timestamped message to the backup_manager.log file"""
    timestamp = datetime.now().strftime("[%d/%m/%Y %H:%M]")
    log_entry = f"{timestamp} {message}\n"
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Write to log file
    with open("logs/backup_manager.log", "a") as log_file:
        log_file.write(log_entry)

def list_schedules():
    """List all backup schedules from backup_schedules.txt"""
    try:
        with open("backup_schedules.txt", "r") as f:
            schedules = f.readlines()
        
        log_message("Show schedules list")
        for i, schedule in enumerate(schedules):
            print(f"{i}: {schedule.strip()}")
    except FileNotFoundError:
        log_message("Error: can't find backup_schedules.txt")
        print("Error: can't find backup_schedules.txt")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 backup_manager.py [start|stop|create|list|delete|backups]")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_schedules()
    else:
        print(f"Command '{command}' not implemented yet")
        log_message(f"Command '{command}' not implemented yet")

if __name__ == "__main__":
    main()






