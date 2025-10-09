#!/usr/bin/env python3
"""
Web Dashboard for Ransomware Detection & Recovery Tool

Flask-based web interface providing real-time monitoring, 
system control, and demonstration capabilities.
"""

import os
import sys
import json
import time
import threading
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import subprocess
from pathlib import Path

# Add src directory to path and handle imports
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

try:
    from config_manager import ConfigManager
    from logger import Logger
    from backup_manager import BackupManager
    from recovery_engine import RecoveryEngine
    from file_monitor import FileSystemMonitor
    from threat_detector import ThreatDetector
    from automated_response import AutomatedResponseSystem
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all source files are present in the src/ directory")
    sys.exit(1)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ransomware_detection_dashboard_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for system state
monitoring_system = None
system_stats = {
    'status': 'stopped',
    'threats_detected': 0,
    'files_monitored': 0,
    'backups_created': 0,
    'recoveries_performed': 0,
    'uptime': 0,
    'last_activity': None,
    'recent_events': []
}

class WebMonitoringSystem:
    """Wrapper for the monitoring system with web interface integration"""
    
    def __init__(self):
        self.config_manager = None
        self.logger = None
        self.file_monitor = None
        self.threat_detector = None
        self.backup_manager = None
        self.recovery_engine = None
        self.automated_response = None
        self.is_running = False
        self.start_time = None
        self.stats_thread = None
        
    def initialize(self):
        """Initialize all system components"""
        try:
            # Load configuration
            self.config_manager = ConfigManager('config.json')
            config = self.config_manager.load_config()
            
            # Initialize logger
            self.logger = Logger(
                log_directory=config.get('log_directory', './logs'),
                log_level='INFO'
            )
            
            # Create directories
            monitored_dir = Path(config.get('monitored_directory', './test_files'))
            backup_dir = Path(config.get('backup_directory', './backups'))
            monitored_dir.mkdir(exist_ok=True)
            backup_dir.mkdir(exist_ok=True)
            
            # Initialize components
            self.file_monitor = FileSystemMonitor(self.logger, str(monitored_dir))
            
            self.threat_detector = ThreatDetector(
                logger=self.logger,
                detection_threshold=config.get('detection_threshold', 5),
                time_window_seconds=config.get('time_window_seconds', 10),
                suspicious_extensions=config.get('suspicious_extensions', [])
            )
            
            self.backup_manager = BackupManager(
                backup_directory=str(backup_dir),
                retention_count=config.get('backup_retention', 5)
            )
            
            self.recovery_engine = RecoveryEngine(self.backup_manager, self.logger)
            
            self.automated_response = AutomatedResponseSystem(
                file_monitor=self.file_monitor,
                threat_detector=self.threat_detector,
                backup_manager=self.backup_manager,
                recovery_engine=self.recovery_engine,
                logger=self.logger,
                response_threshold=config.get('response_threshold', 50)
            )
            
            return True
            
        except Exception as e:
            print(f"Error initializing system: {e}")
            return False
    
    def start_monitoring(self):
        """Start the monitoring system"""
        if self.is_running:
            return False
            
        try:
            if not self.file_monitor.start_monitoring():
                return False
                
            if not self.automated_response.start_automated_response():
                self.file_monitor.stop_monitoring()
                return False
            
            self.is_running = True
            self.start_time = time.time()
            
            # Start stats update thread
            self.stats_thread = threading.Thread(target=self._update_stats_loop, daemon=True)
            self.stats_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error starting monitoring: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        if not self.is_running:
            return False
            
        try:
            self.automated_response.stop_automated_response()
            self.file_monitor.stop_monitoring()
            self.is_running = False
            return True
            
        except Exception as e:
            print(f"Error stopping monitoring: {e}")
            return False
    
    def get_system_stats(self):
        """Get current system statistics"""
        if not self.is_running or not self.automated_response:
            return system_stats
        
        try:
            response_stats = self.automated_response.get_response_statistics()
            backup_stats = self.backup_manager.get_backup_statistics()
            recovery_stats = self.recovery_engine.get_recovery_statistics()
            
            uptime = int(time.time() - self.start_time) if self.start_time else 0
            
            return {
                'status': 'running' if self.is_running else 'stopped',
                'threats_detected': response_stats.get('total_threats_detected', 0),
                'files_monitored': len(self.file_monitor.get_monitored_files()) if hasattr(self.file_monitor, 'get_monitored_files') else 0,
                'backups_created': backup_stats.get('total_backup_versions', 0),
                'recoveries_performed': recovery_stats.get('successful_recoveries', 0),
                'uptime': uptime,
                'last_activity': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_threshold': response_stats.get('response_threshold', 50),
                'success_rate': recovery_stats.get('success_rate_percent', 0),
                'backup_size': backup_stats.get('total_backup_size_bytes', 0)
            }
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            return system_stats
    
    def _update_stats_loop(self):
        """Background thread to update statistics"""
        while self.is_running:
            try:
                current_stats = self.get_system_stats()
                
                # Emit stats to web clients
                socketio.emit('stats_update', current_stats)
                
                # Check for new events
                if hasattr(self.threat_detector, 'get_recent_events'):
                    recent_events = self.threat_detector.get_recent_events()
                    if recent_events:
                        socketio.emit('new_events', recent_events)
                
                time.sleep(2)  # Update every 2 seconds
                
            except Exception as e:
                print(f"Error in stats update loop: {e}")
                time.sleep(5)

# Initialize global monitoring system
monitoring_system = WebMonitoringSystem()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """Get system status"""
    if monitoring_system.is_running:
        stats = monitoring_system.get_system_stats()
    else:
        stats = system_stats.copy()
        stats['status'] = 'stopped'
    
    return jsonify(stats)

@app.route('/api/start', methods=['POST'])
def api_start():
    """Start monitoring system"""
    if not monitoring_system.initialize():
        return jsonify({'success': False, 'message': 'Failed to initialize system'})
    
    if monitoring_system.start_monitoring():
        return jsonify({'success': True, 'message': 'Monitoring started successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to start monitoring'})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """Stop monitoring system"""
    if monitoring_system.stop_monitoring():
        return jsonify({'success': True, 'message': 'Monitoring stopped successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to stop monitoring'})

@app.route('/api/config')
def api_config():
    """Get current configuration"""
    try:
        config_manager = ConfigManager('config.json')
        config = config_manager.load_config()
        return jsonify({'success': True, 'config': config})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/config', methods=['POST'])
def api_update_config():
    """Update configuration"""
    try:
        new_config = request.json
        
        # Validate configuration
        config_manager = ConfigManager('config.json')
        config_manager.config = new_config
        
        # Save configuration
        with open('config.json', 'w') as f:
            json.dump(new_config, f, indent=2)
        
        return jsonify({'success': True, 'message': 'Configuration updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    """Run ransomware simulation"""
    try:
        data = request.json
        attack_type = data.get('attack_type', 'crypto_locker')
        intensity = data.get('intensity', 'moderate')
        
        # Run simulation in background
        def run_simulation():
            try:
                cmd = [
                    sys.executable, 
                    'src/ransomware_simulator.py', 
                    attack_type, 
                    '--intensity', intensity,
                    '--no-cleanup'
                ]
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                
                # Emit completion event
                socketio.emit('simulation_complete', {
                    'attack_type': attack_type,
                    'intensity': intensity,
                    'success': True
                })
                
            except Exception as e:
                socketio.emit('simulation_complete', {
                    'attack_type': attack_type,
                    'intensity': intensity,
                    'success': False,
                    'error': str(e)
                })
        
        thread = threading.Thread(target=run_simulation, daemon=True)
        thread.start()
        
        return jsonify({'success': True, 'message': f'Simulation started: {attack_type} ({intensity})'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/logs')
def api_logs():
    """Get recent log entries"""
    try:
        log_file = Path('./logs/ransomware_detection.log')
        if not log_file.exists():
            return jsonify({'success': True, 'logs': []})
        
        # Read last 50 lines
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_lines = lines[-50:] if len(lines) > 50 else lines
        
        logs = []
        for line in recent_lines:
            line = line.strip()
            if line:
                logs.append(line)
        
        return jsonify({'success': True, 'logs': logs})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/backups')
def api_backups():
    """Get backup information"""
    try:
        backup_dir = Path('./backups')
        if not backup_dir.exists():
            return jsonify({'success': True, 'backups': []})
        
        backups = []
        for backup_file in backup_dir.rglob('*'):
            if backup_file.is_file():
                stat = backup_file.stat()
                backups.append({
                    'name': backup_file.name,
                    'path': str(backup_file.relative_to(backup_dir)),
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({'success': True, 'backups': backups[:20]})  # Last 20 backups
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    # Send current stats to new client
    if monitoring_system.is_running:
        stats = monitoring_system.get_system_stats()
        emit('stats_update', stats)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    print("=" * 60)
    print("RANSOMWARE DETECTION TOOL - WEB DASHBOARD")
    print("=" * 60)
    print("Starting web server...")
    print("Dashboard will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run the Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)