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

def create_schedule(schedule_str):
    """Create a new backup schedule"""
    # Validate schedule format: file_name;hour:minutes;backup_file_name
    parts = schedule_str.split(';')
    if len(parts) != 3 or not parts[0] or not parts[1] or not parts[2]:
        log_message(f"Error: malformed schedule: {schedule_str}")
        print(f"Error: malformed schedule: {schedule_str}")
        return
    
    # Validate time format
    try:
        time_parts = parts[1].split(':')
        if len(time_parts) != 2:
            raise ValueError
        hour, minute = int(time_parts[0]), int(time_parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
    except ValueError:
        log_message(f"Error: malformed schedule: {schedule_str}")
        print(f"Error: malformed schedule: {schedule_str}")
        return
    
    # Add schedule to file
    with open("backup_schedules.txt", "a") as f:
        f.write(schedule_str + "\n")
    
    log_message(f"New schedule added: {schedule_str}")
    print(f"Schedule added: {schedule_str}")

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
    elif command == "create":
        if len(sys.argv) < 3:
            print("Usage: python3 backup_manager.py create [schedule]")
            return
        create_schedule(sys.argv[2])
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python3 backup_manager.py delete [index]")
            return
        delete_schedule(sys.argv[2])
    else:
        print(f"Command '{command}' not implemented yet")
        log_message(f"Command '{command}' not implemented yet")

if __name__ == "__main__":
    main()






