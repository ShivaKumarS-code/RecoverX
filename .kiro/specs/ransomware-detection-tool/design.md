# Design Document

## Overview

The Ransomware Detection & Recovery Tool is a Python-based security application designed as a final year CSE project that demonstrates cybersecurity concepts through practical implementation. The system provides basic real-time file system monitoring, simple threat detection based on file activity patterns, and automated backup/recovery capabilities. The focus is on creating a working prototype that showcases security programming skills while being achievable within academic project constraints.

## Architecture

The system follows a simplified modular architecture suitable for student implementation:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │    │   File Monitor  │    │  Backup Manager │
│   (argparse)    │◄──►│   (watchdog)    │◄──►│  (file copying) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Config File   │    │ Simple Detector │    │ Recovery Engine │
│   (JSON/INI)    │    │ (pattern-based) │    │ (file restore)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │ Logging System  │
                    │ (Python logging)│
                    └─────────────────┘
```

## Components and Interfaces

### 1. File System Monitor
- **Technology**: Python watchdog library (easy to install via pip)
- **Responsibility**: Monitor specified directories for file changes
- **Key Methods**:
  - `start_monitoring(directory: str)`: Begin monitoring single directory
  - `on_modified(event)`: Handle file modification events
  - `stop_monitoring()`: Clean shutdown of monitoring

### 2. Simple Threat Detection Engine
- **Responsibility**: Basic pattern-based ransomware detection suitable for academic demonstration
- **Detection Rules** (Student-friendly):
  - File modification rate: >5 files modified in 10 seconds
  - Suspicious extensions: Files changing to .encrypted, .locked, .crypto
  - File size changes: Significant size increases (potential encryption)
- **Key Methods**:
  - `check_modification_rate()`: Count recent file modifications
  - `is_suspicious_extension(filename)`: Check against known ransomware extensions
  - `evaluate_threat()`: Simple scoring system (0-100)#
## 3. Backup Manager
- **Technology**: Simple file copying with timestamp-based versioning
- **Responsibility**: Create and manage basic backups
- **Key Methods**:
  - `create_backup(file_path: str)`: Copy file to backup directory with timestamp
  - `verify_backup(backup_path: str)`: Check file exists and matches size
  - `list_backups(original_file: str)`: Show available backup versions
  - `cleanup_old_backups()`: Keep only last 5 versions per file

### 4. Recovery Engine
- **Responsibility**: Restore files from backups when threats detected
- **Key Methods**:
  - `restore_file(file_path: str)`: Restore from most recent backup
  - `restore_multiple(file_list: List[str])`: Batch restore operation
  - `verify_restoration(file_path: str)`: Confirm restoration success

### 5. Configuration Manager
- **Technology**: JSON configuration file
- **Configuration Options**:
  - `monitored_directory`: Single directory to monitor
  - `backup_directory`: Where to store backups
  - `alert_email`: Email for notifications (optional)
  - `detection_threshold`: Number of files modified to trigger alert
  - `backup_retention`: Number of backup versions to keep

### 6. Logging System
- **Technology**: Python's built-in logging module
- **Responsibility**: Record system activities and alerts
- **Key Features**:
  - File-based logging with rotation
  - Console output for real-time monitoring
  - Different log levels (INFO, WARNING, CRITICAL)

## Data Models (Simplified)

### File Event
```python
@dataclass
class FileEvent:
    timestamp: datetime
    file_path: str
    event_type: str  # 'modified', 'created', 'deleted'
    file_size: int
```

### Backup Record
```python
@dataclass
class BackupRecord:
    original_path: str
    backup_path: str
    timestamp: datetime
    file_size: int
```

### Detection Result
```python
@dataclass
class DetectionResult:
    is_threat: bool
    threat_score: int  # 0-100
    affected_files: List[str]
    detection_reason: str
```

## Error Handling (Student-Appropriate)

### File System Errors
- Handle permission denied with clear error messages
- Skip files that can't be accessed and continue monitoring
- Log errors but don't crash the application

### Backup Errors
- Check disk space before creating backups
- Handle backup directory creation if it doesn't exist
- Provide clear error messages for backup failures

### Recovery Errors
- Verify backup exists before attempting restoration
- Handle cases where backup is corrupted or missing
- Provide status updates during recovery operations

## Testing Strategy (Academic Focus)

### Manual Testing
- Create test files and modify them rapidly to trigger detection
- Test backup creation and restoration manually
- Verify logging output and configuration loading

### Automated Testing (Optional)
- Unit tests for core detection logic
- Test backup and recovery with sample files
- Configuration validation tests

### Demonstration Scenarios
- Simulate ransomware by rapidly encrypting test files
- Show real-time detection and automatic recovery
- Display logging output and system responses

## Implementation Considerations for Students

### Technology Stack (Simplified)
**Required Libraries:**
- `watchdog`: File system monitoring (pip install watchdog)
- `argparse`: Command-line interface (built-in)
- `logging`: System logging (built-in)
- `json`: Configuration management (built-in)
- `shutil`: File operations (built-in)
- `datetime`: Timestamps (built-in)

**Optional Libraries:**
- `smtplib`: Email alerts (built-in, requires email setup)
- `hashlib`: File integrity checking (built-in)

### Project Scope (Realistic for Students)
**Core Features (Must Have):**
- Monitor single directory for file changes
- Detect rapid file modifications (simple threshold)
- Create timestamped backups of modified files
- Restore files when threat detected
- Basic logging and console output

**Advanced Features (Nice to Have):**
- Email alerts
- GUI interface with tkinter
- File integrity verification with hashes
- Configuration file management
- Multiple directory monitoring

### Development Timeline (Suggested)
**Week 1-2:** Set up file monitoring with watchdog
**Week 3-4:** Implement basic threat detection logic
**Week 5-6:** Add backup and recovery functionality
**Week 7-8:** Implement logging and configuration
**Week 9-10:** Testing, documentation, and demonstration prep

### Academic Value
**Skills Demonstrated:**
- File system programming in Python
- Event-driven programming concepts
- Basic cybersecurity threat detection
- Error handling and logging
- Configuration management
- Testing and validation

**Resume-Worthy Outcomes:**
- Real-time system monitoring implementation
- Automated backup and recovery system
- Security threat detection algorithms
- Python application development
- System administration concepts