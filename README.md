# Ransomware Detection & Recovery Tool

A Python-based security application designed to monitor file systems for suspicious activities indicative of ransomware attacks and provide automated backup and recovery capabilities. This project demonstrates cybersecurity concepts through practical implementation, featuring real-time monitoring, threat detection, and automated recovery systems.

## 🚀 Features

- **Real-time File System Monitoring**: Continuously monitors specified directories for file changes
- **Intelligent Threat Detection**: Pattern-based detection of ransomware-like activities
- **Automated Backup System**: Creates timestamped backups with configurable retention
- **Automated Recovery**: Restores files from backups when threats are detected
- **Web Dashboard**: Professional web interface with real-time monitoring and controls
- **Interactive Demonstrations**: Built-in ransomware simulation with web-based controls
- **Comprehensive Logging**: Detailed logging of all system activities and security events
- **Command-line Interface**: Easy-to-use CLI for system management
- **Real-time Statistics**: Live charts and metrics for system performance

## 📁 Project Structure

```
ransomware-detection-tool/
├── main.py                          # Main entry point and CLI
├── web_app.py                       # Web dashboard application
├── start_dashboard.py               # Dashboard startup script
├── demo.py                          # Comprehensive demonstration script
├── config.json                      # Configuration file
├── requirements.txt                 # Python dependencies
├── templates/                       # Web dashboard templates
│   └── dashboard.html              # Main dashboard interface
├── src/                            # Source code
│   ├── __init__.py
│   ├── automated_response.py       # Automated response system
│   ├── backup_manager.py           # Backup creation and management
│   ├── config_manager.py           # Configuration management
│   ├── demo_automated_response.py  # Response system demo
│   ├── demo_recovery.py            # Recovery system demo
│   ├── file_monitor.py             # File system monitoring
│   ├── logger.py                   # Logging system
│   ├── ransomware_simulator.py     # Ransomware simulation tool
│   ├── recovery_engine.py          # File recovery system
│   └── threat_detector.py          # Threat detection engine
├── logs/                           # Log files (auto-created)
├── backups/                        # Backup storage (auto-created)
└── test_files/                     # Test directory for monitoring
```

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup
1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Quick Start

### 1. Web Dashboard (Recommended)
```bash
# Start the web dashboard
python start_dashboard.py
```
Then open your browser to `http://localhost:5000` for the full web interface with:
- Real-time monitoring controls
- Interactive ransomware simulation
- Live statistics and charts
- System logs and backup management

### 2. Command Line Interface
```bash
# Start monitoring with default configuration
python main.py start

# Check system status
python main.py status

# Stop monitoring
python main.py stop
```

### 3. Complete Demonstration
```bash
# Run comprehensive demonstration
python demo.py
```

### 4. Manual Ransomware Simulation
```bash
# Simulate different types of ransomware attacks
python src/ransomware_simulator.py crypto_locker --intensity moderate
python src/ransomware_simulator.py rapid_encryptor --intensity heavy
```

## ⚙️ Configuration

Edit `config.json` to customize system behavior:

```json
{
  "monitored_directory": "./test_files",
  "backup_directory": "./backups",
  "log_directory": "./logs",
  "detection_threshold": 5,
  "time_window_seconds": 10,
  "response_threshold": 50,
  "backup_retention": 5,
  "suspicious_extensions": [
    ".encrypted", ".locked", ".crypto", ".vault", ".secure"
  ],
  "alert_email": "admin@example.com"
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `monitored_directory` | Directory to monitor for changes | `./test_files` |
| `backup_directory` | Where to store backups | `./backups` |
| `log_directory` | Where to store log files | `./logs` |
| `detection_threshold` | Files modified to trigger alert | `5` |
| `time_window_seconds` | Time window for detection | `10` |
| `response_threshold` | Threat score to trigger response | `50` |
| `backup_retention` | Number of backup versions to keep | `5` |
| `suspicious_extensions` | File extensions indicating encryption | See config |
| `alert_email` | Email for notifications (optional) | `null` |

## 🎮 Demonstration & Testing

### Web Dashboard (Best for Interviews)
```bash
python start_dashboard.py
```
Professional web interface featuring:
- **Real-time Monitoring**: Live system status and statistics
- **Interactive Controls**: Start/stop monitoring with one click
- **Ransomware Simulation**: Web-based attack simulation controls
- **Live Charts**: Real-time data visualization
- **System Logs**: Live log streaming and filtering
- **Backup Management**: Visual backup status and history

### Interactive Demo Launcher
```bash
python run_demo.py
```
Command-line menu with options for:
- Complete system demonstration
- Individual component testing
- Custom ransomware simulations
- System status monitoring
- Help and documentation

### Complete System Demonstration
```bash
python demo.py
```
This runs a comprehensive demonstration showing:
- File system monitoring setup
- Normal file activity (no alerts)
- Simulated ransomware attack
- Automated threat detection
- Backup creation and recovery
- System statistics and reporting

### Ransomware Simulation Tool
```bash
# Different attack types
python src/ransomware_simulator.py crypto_locker    # Encrypts and renames files
python src/ransomware_simulator.py file_renamer     # Renames with random extensions
python src/ransomware_simulator.py rapid_encryptor  # Fast attack (triggers detection)
python src/ransomware_simulator.py stealth_encryptor # Slow attack (may avoid detection)

# Different intensities
python src/ransomware_simulator.py crypto_locker --intensity light     # Slow, few files
python src/ransomware_simulator.py crypto_locker --intensity moderate  # Normal speed
python src/ransomware_simulator.py crypto_locker --intensity heavy     # Fast, many files
```

### Individual Component Demos
```bash
# Test automated response system
python src/demo_automated_response.py

# Test recovery engine
python src/demo_recovery.py
```

## 🌐 Web Dashboard Interface

### Starting the Dashboard
```bash
python start_dashboard.py          # Auto-opens browser to http://localhost:5000
# OR
python web_app.py                  # Manual start (navigate to localhost:5000)
```

### Dashboard Features
- **System Control Panel**: Start/stop monitoring with visual status indicators
- **Real-time Statistics**: Live updating charts and metrics
- **Threat Simulation**: Interactive ransomware attack simulation
- **Backup Viewer**: Visual backup history and file management
- **Live Log Stream**: Real-time system logs with filtering
- **Configuration Management**: Web-based settings adjustment
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices

### Perfect for Demonstrations
The web dashboard is ideal for:
- **Job Interviews**: Professional visual interface
- **Presentations**: Real-time data visualization
- **Training Sessions**: Interactive learning environment
- **System Monitoring**: Production-ready monitoring interface

## 🖥️ Command Line Interface

### Main Commands
```bash
python main.py start [options]     # Start monitoring system
python main.py stop                # Stop monitoring system
python main.py status              # Show system status
python main.py config              # Display current configuration
python main.py validate            # Validate configuration
```

### Options
```bash
--config FILE          # Use custom configuration file
--log-level LEVEL      # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
--daemon               # Run in background mode
```

### Examples
```bash
# Start with custom config and debug logging
python main.py start --config production.json --log-level DEBUG

# Check status with verbose output
python main.py status

# Validate configuration before starting
python main.py validate
```

## 🔍 How It Works

### 1. File System Monitoring
- Uses Python's `watchdog` library for real-time file system events
- Monitors specified directories for file modifications, creations, and deletions
- Tracks file access patterns and modification rates

### 2. Threat Detection
The system detects potential ransomware through multiple indicators:
- **Rapid File Modifications**: Multiple files modified in short time window
- **Suspicious Extensions**: Files renamed with known ransomware extensions
- **File Size Changes**: Significant changes in file sizes (encryption indicators)
- **Pattern Recognition**: Behavioral patterns typical of ransomware

### 3. Automated Response
When threats are detected:
- **Immediate Backup**: Creates emergency backups of affected files
- **Threat Assessment**: Calculates threat score based on multiple factors
- **Automated Recovery**: Restores files if threat score exceeds threshold
- **Logging & Alerts**: Records all activities and sends notifications

### 4. Recovery System
- **Backup Management**: Maintains versioned backups with configurable retention
- **Integrity Verification**: Verifies backup and restored file integrity
- **Multiple Recovery Options**: Automatic and manual recovery modes
- **Rollback Capability**: Can restore from different backup versions

## 📊 System Monitoring

### Real-time Status Display
When running `python main.py start`, the system shows:
- Current monitoring status
- Detection statistics
- Response activities
- System health indicators

### Log Files
The system generates detailed logs in the `logs/` directory:
- `ransomware_detection.log`: Main system log
- Rotating logs with timestamps
- Different log levels for debugging and monitoring

### Statistics and Reporting
Access system statistics through:
```bash
python main.py status  # Current system status and statistics
```

## 🛡️ Security Features

### Detection Capabilities
- **Real-time Monitoring**: Immediate detection of suspicious activities
- **Pattern-based Detection**: Recognizes common ransomware behaviors
- **Configurable Thresholds**: Adjustable sensitivity for different environments
- **False Positive Reduction**: Smart filtering to reduce false alarms

### Protection Mechanisms
- **Automated Backups**: Continuous backup of monitored files
- **Rapid Response**: Quick reaction to detected threats
- **File Recovery**: Automatic restoration from clean backups
- **System Isolation**: Can isolate affected files during attacks

## 🔧 Development & Customization

### Adding New Detection Rules
Extend the `ThreatDetector` class in `src/threat_detector.py`:
```python
def custom_detection_rule(self, file_events):
    # Implement custom detection logic
    pass
```

### Custom Response Actions
Modify the `AutomatedResponseSystem` class in `src/automated_response.py`:
```python
def custom_response_action(self, threat_info):
    # Implement custom response logic
    pass
```

### Configuration Extensions
Add new configuration options in `config.json` and update `ConfigManager`.

## 📚 Educational Value

This project demonstrates key cybersecurity concepts:

### Technical Skills
- **File System Programming**: Real-time monitoring and event handling
- **Security Pattern Recognition**: Identifying malicious behavior patterns
- **Automated Response Systems**: Building reactive security systems
- **Data Protection**: Backup and recovery system implementation
- **System Administration**: Configuration management and logging

### Cybersecurity Concepts
- **Ransomware Behavior Analysis**: Understanding attack patterns
- **Incident Response**: Automated threat response procedures
- **Data Recovery**: Business continuity and disaster recovery
- **Security Monitoring**: Real-time threat detection systems
- **Defense in Depth**: Multiple layers of protection

## ✅ Project Status: COMPLETE

This ransomware detection and recovery tool is **fully implemented and ready to use**. All planned features have been developed, tested, and documented.

### What's Included
- ✅ **Complete Source Code**: All 8 core components fully implemented
- ✅ **Comprehensive Testing**: Multiple demonstration and simulation tools
- ✅ **Full Documentation**: README, demo guides, and inline code documentation
- ✅ **Configuration System**: Flexible JSON-based configuration with validation
- ✅ **Command-Line Interface**: Full CLI with all essential commands
- ✅ **Educational Materials**: Step-by-step guides and learning resources

### Ready for Use
- **Immediate Deployment**: No additional development required
- **Educational Ready**: Perfect for classroom use and training
- **Demonstration Ready**: Multiple demo scenarios available
- **Customization Ready**: Well-documented code for extensions
- **Research Ready**: Solid foundation for advanced security research

## 🚨 Important Notes

### Educational Purpose
This tool is designed for educational and demonstration purposes. While it implements real security concepts, it should not be used as the sole protection against actual ransomware attacks in production environments.

### System Requirements
- Sufficient disk space for backups
- Appropriate file system permissions
- Python 3.7+ with required dependencies

### Performance Considerations
- Monitor system resources when watching large directories
- Configure appropriate backup retention to manage disk usage
- Adjust detection thresholds based on system performance

## 🤝 Contributing

This project welcomes contributions for educational enhancement:
- Additional detection algorithms
- New demonstration scenarios
- Performance improvements
- Documentation updates

## 📄 License

This project is intended for educational use. Please ensure compliance with your institution's policies and local regulations when using or modifying this code.

## 🆘 Troubleshooting

### Common Issues

**Monitoring won't start:**
- Check file permissions on monitored directory
- Verify configuration file is valid JSON
- Ensure all dependencies are installed

**No backups created:**
- Check backup directory permissions
- Verify sufficient disk space
- Review log files for error messages

**Detection not working:**
- Adjust detection threshold in configuration
- Check if files are being modified in monitored directory
- Review threat detection logs

**Recovery fails:**
- Ensure backup files exist and are accessible
- Check file permissions for restoration
- Verify backup integrity

### Getting Help
1. Check log files in `logs/` directory
2. Run `python main.py validate` to check configuration
3. Use `python main.py status` to check system state
4. Review error messages in console output
5. Consult `DEMO_GUIDE.md` for detailed demonstration instructions

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Launch Web Dashboard
```bash
python start_dashboard.py
```
This automatically opens your browser to the professional web interface.

### Step 3: Start Demonstrating
- Click "Start Monitoring" in the web dashboard
- Run ransomware simulations with the web controls
- Watch real-time threat detection and response
- Show live statistics and system logs

**Perfect for Interviews!** The web dashboard provides a professional, visual interface that showcases your full-stack development skills alongside cybersecurity expertise.

### Alternative: Command Line Demo
```bash
python run_demo.py              # Interactive command-line demo
python demo.py                  # Complete automated demonstration
```

## 🎓 Project Highlights

### Core Components Implemented
- **Web Dashboard**: Professional Flask-based interface with real-time monitoring
- **File System Monitor**: Real-time monitoring using Python watchdog library
- **Threat Detection Engine**: Multi-factor ransomware behavior analysis
- **Backup Manager**: Automated, versioned backup system with integrity verification
- **Recovery Engine**: Intelligent file restoration with multiple recovery modes
- **Automated Response System**: Integrated threat response and recovery automation
- **Interactive Simulation**: Web-based ransomware attack simulation controls
- **Command-Line Interface**: Full-featured CLI with real-time monitoring display
- **Demonstration Suite**: Comprehensive testing and educational tools

### Key Achievements
- **Professional Web Interface**: Modern, responsive dashboard perfect for interviews
- **Real-time Data Visualization**: Live charts and statistics using Chart.js
- **Full-Stack Implementation**: Flask backend with WebSocket real-time updates
- **Zero-Configuration Setup**: Works out of the box with sensible defaults
- **Educational Focus**: Designed specifically for cybersecurity learning
- **Safe Testing Environment**: Simulated attacks with no actual malware
- **Production-Ready Code**: Professional-grade implementation with error handling
- **Comprehensive Documentation**: Complete guides for users and developers
- **Interactive Demonstrations**: Multiple demo modes for different learning scenarios

### Technical Excellence
- **Modular Architecture**: Clean separation of concerns with well-defined interfaces
- **Robust Error Handling**: Graceful failure recovery and detailed error reporting
- **Configurable Parameters**: Extensive customization options for different environments
- **Performance Optimized**: Efficient file monitoring with minimal system impact
- **Comprehensive Logging**: Detailed audit trail of all system activities
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux

## 🌟 Use Cases

### Educational Applications
- **Cybersecurity Courses**: Hands-on learning of threat detection concepts
- **Security Training**: Practical demonstration of ransomware behavior
- **Research Projects**: Foundation for advanced security research
- **Workshops & Seminars**: Interactive security awareness training

### Professional Development
- **Security Team Training**: Understanding automated response systems
- **Incident Response Planning**: Learning recovery procedures
- **Tool Development**: Reference implementation for security tools
- **Proof of Concept**: Demonstrating security monitoring capabilities

### Academic Research
- **Behavioral Analysis**: Studying ransomware attack patterns
- **Detection Algorithms**: Testing new threat detection methods
- **Response Strategies**: Evaluating automated response effectiveness
- **System Performance**: Analyzing monitoring system efficiency