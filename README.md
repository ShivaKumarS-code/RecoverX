# Ransomware Detection & Recovery Tool

A Python-based security application designed to monitor file systems for suspicious activities indicative of ransomware attacks and provide automated backup and recovery capabilities.

## Project Structure

```
ransomware-detection-tool/
├── main.py                 # Main entry point
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── src/                   # Source code
│   ├── __init__.py
│   ├── config_manager.py  # Configuration management
│   └── logger.py          # Logging system
├── logs/                  # Log files (auto-created)
├── backups/              # Backup storage (auto-created)
└── test_files/           # Test directory for monitoring
```

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Start monitoring
```bash
python main.py start
```

### Check system status
```bash
python main.py status
```

### View configuration
```bash
python main.py config
```

### Stop monitoring
```bash
python main.py stop
```

### Command line options
```bash
python main.py start --config custom.json --log-level DEBUG
```

## Configuration

Edit `config.json` to customize:
- `monitored_directory`: Directory to monitor for changes
- `backup_directory`: Where to store backups
- `detection_threshold`: Number of files modified to trigger alert
- `suspicious_extensions`: File extensions that indicate encryption

## Development Status

- [x] Task 1: Project structure and basic configuration
- [ ] Task 2: File system monitoring
- [ ] Task 3: Threat detection engine
- [ ] Task 4: Backup system
- [ ] Task 5: Recovery engine
- [ ] Task 6: Automated response integration
- [ ] Task 7: Command-line interface enhancement
- [ ] Task 8: Demonstration capabilities