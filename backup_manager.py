#!/usr/bin/env python3
import sys
import os
import subprocess
import signal
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

def delete_schedule(index_str):
    """Delete a backup schedule by index"""
    try:
        index = int(index_str)
    except ValueError:
        log_message(f"Error: invalid index: {index_str}")
        print(f"Error: invalid index: {index_str}")
        return
    
    try:
        with open("backup_schedules.txt", "r") as f:
            schedules = f.readlines()
        
        if index < 0 or index >= len(schedules):
            log_message(f"Error: can't find schedule at index {index}")
            print(f"Error: can't find schedule at index {index}")
            return
        
        # Remove the schedule at the specified index
        schedules.pop(index)
        
        # Write back to file
        with open("backup_schedules.txt", "w") as f:
            f.writelines(schedules)
        
        log_message(f"Schedule at index {index} deleted")
        print(f"Schedule at index {index} deleted")
        
    except FileNotFoundError:
        log_message("Error: can't find backup_schedules.txt")
        print("Error: can't find backup_schedules.txt")

def get_service_pid():
    """Get the PID of the running backup_service.py process"""
    try:
        result = subprocess.run(["ps", "-A", "-f"], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'backup_service.py' in line and 'python' in line:
                parts = line.split()
                return int(parts[1])  # PID is the second column
    except:
        pass
    return None

def start_service():
    """Start the backup service in background"""
    if get_service_pid():
        log_message("Error: backup_service already running")
        print("Error: backup_service already running")
        return
    
    try:
        subprocess.Popen(["python3", "backup_service.py"], start_new_session=True)
        log_message("backup_service started")
        print("backup_service started")
    except Exception as e:
        log_message("Error: can't start backup_service")
        print("Error: can't start backup_service")

def stop_service():
    """Stop the backup service"""
    pid = get_service_pid()
    if not pid:
        log_message("Error: backup_service not running")
        print("Error: backup_service not running")
        return
    
    try:
        os.kill(pid, signal.SIGTERM)
        log_message("backup_service stopped")
        print("backup_service stopped")
    except Exception as e:
        log_message("Error: can't stop backup_service")
        print("Error: can't stop backup_service")

def list_backups():
    """List all backup files in ./backups directory"""
    try:
        backup_files = os.listdir("backups")
        log_message("Show backups list")
        for backup_file in sorted(backup_files):
            print(backup_file)
    except FileNotFoundError:
        log_message("Error: can't find backups directory")
        print("Error: can't find backups directory")

def list_schedules():
    """List all backup schedules from backup_schedules.txt"""
    try:
        with open("backup_schedules.txt", "r") as f:
            schedules = f.readlines()
        
        log_message("Show schedules list:")
        for i, schedule in enumerate(schedules):
            log_message(f"{i}: {schedule.strip()}")
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
    elif command == "backups":
        list_backups()
    elif command == "start":
        start_service()
    elif command == "stop":
        stop_service()
    else:
        print(f"Command '{command}' not implemented yet")
        log_message(f"Command '{command}' not implemented yet")

if __name__ == "__main__":
    main()






