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

def main():
    """Main service loop"""
    log_message("backup_service started")

if __name__ == "__main__":
    main()