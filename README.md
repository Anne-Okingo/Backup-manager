# Backup Manager

A Python-based backup management system that schedules and performs automated backups of directories.

## Features

- Schedule automated backups at specific times
- Background service for continuous monitoring
- Compressed tar archive backups
- Comprehensive logging system
- Command-line interface for easy management

## Files

- `backup_manager.py` - Main controller script
- `backup_service.py` - Background service daemon
- `backup_schedules.txt` - Schedule configuration file
- `logs/` - Log files directory
- `backups/` - Backup files directory

## Usage

### Commands

```bash
# Create a new backup schedule
python3 backup_manager.py create "source_path;HH:MM;backup_name"

# List all scheduled backups
python3 backup_manager.py list

# Delete a schedule by index
python3 backup_manager.py delete [index]

# Start the backup service
python3 backup_manager.py start

# Stop the backup service
python3 backup_manager.py stop

# List backup files
python3 backup_manager.py backups
```

### Schedule Format

Schedules use the format: `source_path;time;backup_name`
- `source_path` - Directory to backup
- `time` - Time in HH:MM format (24-hour)
- `backup_name` - Name for the backup file

### Example

```bash
# Create schedules
python3 backup_manager.py create "documents;14:30;daily_docs"
python3 backup_manager.py create "projects;02:00;nightly_backup"

# Start service
python3 backup_manager.py start

# Check backups
python3 backup_manager.py backups
```

## Logging

All operations are logged with timestamps:
- `logs/backup_manager.log` - Manager operations
- `logs/backup_service.log` - Service operations

## Requirements

- Python 3.x
- Standard library modules: `os`, `sys`, `subprocess`, `tarfile`, `datetime`, `time`