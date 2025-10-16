# 🛡️ RecoverX: Ransomware Detection & Recovery

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js">
  <img src="https://img.shields.io/badge/Security-FF0000?style=for-the-badge&logo=security&logoColor=white" alt="Security">
</p>

**RecoverX** is a Python-based security application that monitors file systems for ransomware attacks and provides automated backup and recovery. With real-time detection, intelligent threat analysis, and a professional web dashboard, it demonstrates practical cybersecurity concepts in action.

---

## 🛠️ Tech Stack

<table>
  <tr>
    <td><b>🎨 Frontend</b></td>
    <td>HTML, CSS, JavaScript, Chart.js</td>
  </tr>
  <tr>
    <td><b>⚡ Backend</b></td>
    <td>Python, Flask, WebSocket</td>
  </tr>
  <tr>
    <td><b>🔍 Monitoring</b></td>
    <td>Watchdog (File System Events)</td>
  </tr>
  <tr>
    <td><b>💾 Storage</b></td>
    <td>JSON Configuration, File-based Backups</td>
  </tr>
  <tr>
    <td><b>📊 Visualization</b></td>
    <td>Real-time Charts, Live Statistics</td>
  </tr>
</table>

---

## ✨ Features

<ul>
  <li>🔍 <b>Real-time Monitoring</b> - Continuously watches directories for suspicious changes</li>
  <li>🤖 <b>Intelligent Detection</b> - Pattern-based ransomware behavior analysis</li>
  <li>💾 <b>Automated Backups</b> - Timestamped backups with configurable retention</li>
  <li>🔄 <b>Auto-Recovery</b> - Instant file restoration when threats detected</li>
  <li>📊 <b>Web Dashboard</b> - Professional interface with real-time monitoring</li>
  <li>🎮 <b>Interactive Demos</b> - Built-in ransomware simulation with web controls</li>
  <li>📝 <b>Comprehensive Logging</b> - Detailed audit trail of all activities</li>
  <li>⌨️ <b>CLI Interface</b> - Full-featured command-line management</li>
</ul>

---

## 🏗️ Architecture

### System Overview
```
┌─────────────────────────────────────────────────────────┐
│                    Web Dashboard                         │
│  • Real-time Monitoring   • Threat Simulation           │
│  • Live Statistics        • System Controls             │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │    Flask Web Server     │
        │  • REST API             │
        │  • WebSocket Updates    │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   Core Security Engine  │
        │  ┌──────────────────┐   │
        │  │ File Monitor     │   │
        │  │ (Watchdog)       │   │
        │  └──────────────────┘   │
        │  ┌──────────────────┐   │
        │  │ Threat Detector  │   │
        │  │ (Pattern Analysis)│   │
        │  └──────────────────┘   │
        │  ┌──────────────────┐   │
        │  │ Response System  │   │
        │  │ (Auto Recovery)  │   │
        │  └──────────────────┘   │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   Storage Layer         │
        │  • Backup Manager       │
        │  • Recovery Engine      │
        │  • Version Control      │
        └─────────────────────────┘
```

---

## 📁 Project Structure

```
📦 ransomware-detection-tool/
├── 📄 main.py                          # CLI entry point
├── 📄 web_app.py                       # Web dashboard server
├── 📄 start_dashboard.py               # Dashboard launcher
├── 📄 demo.py                          # Comprehensive demo
├── 📄 config.json                      # System configuration
├── 📄 requirements.txt                 # Dependencies
├── 📂 templates/
│   └── dashboard.html                  # Web interface
├── 📂 src/
│   ├── file_monitor.py                 # File system monitoring
│   ├── threat_detector.py              # Threat detection
│   ├── automated_response.py           # Auto response
│   ├── backup_manager.py               # Backup system
│   ├── recovery_engine.py              # File recovery
│   ├── ransomware_simulator.py         # Attack simulation
│   └── logger.py                       # Logging system
├── 📂 logs/                            # System logs
├── 📂 backups/                         # File backups
└── 📂 test_files/                      # Monitored directory
```

---

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Launch Web Dashboard (Recommended)

```bash
# Start the web dashboard
python start_dashboard.py
```

Access at: **http://localhost:5000**

Features:
- Real-time monitoring controls
- Interactive ransomware simulation
- Live statistics and charts
- System logs viewer
- Backup management

### Command Line Interface

```bash
# Start monitoring
python main.py start

# Check system status
python main.py status

# Stop monitoring
python main.py stop
```

### Run Complete Demo

```bash
# Comprehensive demonstration
python demo.py
```

---

## 🎮 Interactive Demonstrations

### Web Dashboard Demo
```bash
python start_dashboard.py
```
Perfect for presentations and interviews:
- One-click monitoring control
- Visual ransomware simulation
- Real-time data visualization
- Live log streaming

### Ransomware Simulation
```bash
# Different attack types
python src/ransomware_simulator.py crypto_locker
python src/ransomware_simulator.py rapid_encryptor
python src/ransomware_simulator.py stealth_encryptor

# Different intensities
python src/ransomware_simulator.py crypto_locker --intensity light
python src/ransomware_simulator.py crypto_locker --intensity moderate
python src/ransomware_simulator.py crypto_locker --intensity heavy
```

---

## ⚙️ Configuration

### config.json

```json
{
  "monitored_directory": "./test_files",
  "backup_directory": "./backups",
  "detection_threshold": 5,
  "time_window_seconds": 10,
  "response_threshold": 50,
  "backup_retention": 5,
  "suspicious_extensions": [
    ".encrypted", ".locked", ".crypto"
  ]
}
```

### Key Settings

<table>
  <tr>
    <th>Option</th>
    <th>Description</th>
    <th>Default</th>
  </tr>
  <tr>
    <td><b>detection_threshold</b></td>
    <td>Files modified to trigger alert</td>
    <td>5</td>
  </tr>
  <tr>
    <td><b>time_window_seconds</b></td>
    <td>Time window for detection</td>
    <td>10</td>
  </tr>
  <tr>
    <td><b>response_threshold</b></td>
    <td>Threat score to auto-recover</td>
    <td>50</td>
  </tr>
  <tr>
    <td><b>backup_retention</b></td>
    <td>Backup versions to keep</td>
    <td>5</td>
  </tr>
</table>

---

## 🔍 How It Works

### Threat Detection

**System monitors for:**
- 🚨 Rapid file modifications
- 🔐 Suspicious file extensions
- 📊 Abnormal file size changes
- 🎯 Known ransomware patterns

**Detection Process:**
1. File system events captured in real-time
2. Pattern analysis identifies suspicious behavior
3. Threat score calculated based on multiple factors
4. Alert triggered when threshold exceeded

### Automated Response

**When threat detected:**
1. 💾 **Emergency Backup** - Instant backup of affected files
2. 🔍 **Threat Assessment** - Calculate threat severity
3. 🔄 **Auto-Recovery** - Restore files if score > threshold
4. 📝 **Logging** - Record all activities and alerts

### Recovery System

**Backup Features:**
- Versioned backups with timestamps
- Configurable retention policy
- Integrity verification
- Multiple recovery modes

---

## 📊 Web Dashboard Features

### System Control Panel
- Start/Stop monitoring with visual indicators
- Real-time system status display
- Configuration management

### Live Statistics
- File modification tracking
- Threat detection metrics
- Backup and recovery counts
- Performance monitoring

### Threat Simulation
- Interactive attack controls
- Multiple simulation types
- Adjustable intensity levels
- Real-time detection response

### Log Viewer
- Live log streaming
- Filtering and search
- Severity-based highlighting
- Export capabilities

---

## 🛡️ Security Features

### Detection Capabilities
- ✅ Real-time file system monitoring
- ✅ Pattern-based threat recognition
- ✅ Configurable sensitivity
- ✅ False positive reduction

### Protection Mechanisms
- ✅ Automated continuous backups
- ✅ Rapid threat response
- ✅ Automatic file recovery
- ✅ System activity logging

---

## 🎯 Use Cases

### Educational
- 🎓 Cybersecurity courses
- 📚 Security training programs
- 🔬 Research projects
- 💼 Workshops and seminars

### Professional
- 👥 Security team training
- 🚨 Incident response planning
- 🛠️ Tool development reference
- 📈 Proof of concept demos

---

## 📝 Command Reference

### Main Commands

```bash
# System control
python main.py start              # Start monitoring
python main.py stop               # Stop monitoring
python main.py status             # System status

# Configuration
python main.py config             # Show configuration
python main.py validate           # Validate config

# Options
python main.py start --log-level DEBUG
python main.py start --config custom.json
```

### Simulation Commands

```bash
# Attack types
python src/ransomware_simulator.py crypto_locker
python src/ransomware_simulator.py file_renamer
python src/ransomware_simulator.py rapid_encryptor

# Intensity levels
--intensity light      # Slow attack
--intensity moderate   # Normal speed
--intensity heavy      # Fast attack
```

---

## 🐛 Troubleshooting

**Monitoring won't start:**
```bash
# Check permissions
python main.py validate

# Review logs
cat logs/ransomware_detection.log
```

**No backups created:**
```bash
# Verify directory permissions
ls -la backups/

# Check disk space
df -h
```

**Detection not working:**
```bash
# Adjust threshold in config.json
"detection_threshold": 3

# Test with simulation
python src/ransomware_simulator.py rapid_encryptor
```

---

## 🌟 Project Highlights

### Core Components
- 🌐 **Professional Web Dashboard** - Flask-based real-time interface
- 👁️ **File System Monitor** - Watchdog library integration
- 🤖 **Threat Detection Engine** - Multi-factor behavior analysis
- 💾 **Backup Manager** - Versioned backup system
- 🔄 **Recovery Engine** - Intelligent file restoration
- ⚡ **Automated Response** - Integrated threat response
- 🎮 **Interactive Simulation** - Web-based attack controls
- ⌨️ **Command-Line Interface** - Full CLI with monitoring

### Technical Excellence
- ✅ Zero-configuration setup
- ✅ Modular architecture
- ✅ Cross-platform compatible
- ✅ Production-ready code
- ✅ Comprehensive logging
- ✅ Real-time visualization

---

## 🚨 Important Notes

<blockquote>
⚠️ <b>Educational Purpose</b><br>
This tool is designed for educational and demonstration purposes. It implements real security concepts but should not be used as sole protection in production environments.
</blockquote>

### System Requirements
- Python 3.7 or higher
- Sufficient disk space for backups
- Appropriate file system permissions

---

## 🤝 Contributing

Contributions welcome for:
- Additional detection algorithms
- New demonstration scenarios
- Performance improvements
- Documentation updates

---

## 📄 License

This project is intended for educational use. Please ensure compliance with your institution's policies and local regulations.

---

<p align="center">
  <b>Built with ❤️ for Cybersecurity Education</b><br>
  <i>Understanding threats to build better defenses.</i>
</p>
