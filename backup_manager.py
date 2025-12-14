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

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 backup_manager.py [start|stop|create|list|delete|backups]")
        return
    
    command = sys.argv[1]
    print(f"Command received: {command}")
    log_message(f"Command received: {command}")

if __name__ == "__main__":
    main()






