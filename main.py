#!/usr/bin/env python3
"""
Ransomware Detection & Recovery Tool
Main entry point for the application

This tool monitors file systems for suspicious activities indicative of ransomware
attacks and provides automated backup and recovery capabilities.
"""

import argparse
import sys
import os
from src.config_manager import ConfigManager
from src.logger import Logger
from src.backup_manager import BackupManager
from src.recovery_engine import RecoveryEngine
from src.file_monitor import FileSystemMonitor
from src.threat_detector import ThreatDetector
from src.automated_response import AutomatedResponseSystem


def main():
    """Main entry point for the ransomware detection tool"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Ransomware Detection & Recovery Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py start                    # Start monitoring with default config
  python main.py start --config custom.json  # Start with custom config
  python main.py status                   # Check system status
  python main.py stop                     # Stop monitoring
  python main.py config                   # Show current configuration
  python main.py validate                 # Validate configuration settings
        """
    )
    
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'status', 'config', 'validate'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Run in daemon mode (background)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize configuration manager
        config_manager = ConfigManager(args.config)
        config = config_manager.load_config()
        
        # Initialize logging
        logger = Logger(
            log_directory=config.get('log_directory', './logs'),
            log_level=args.log_level
        )
        
        logger.info("=" * 50)
        logger.info("Ransomware Detection Tool Starting")
        logger.info("=" * 50)
        logger.info(f"Command: {args.command}")
        logger.info(f"Config file: {args.config}")
        logger.info(f"Log level: {args.log_level}")
        
        # Execute command
        if args.command == 'start':
            start_monitoring(config_manager, logger, args.daemon)
        elif args.command == 'stop':
            stop_monitoring(logger)
        elif args.command == 'status':
            show_status(config_manager, logger)
        elif args.command == 'config':
            show_config(config_manager, logger)
        elif args.command == 'validate':
            validate_config_command(config_manager, logger)
        
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def start_monitoring(config_manager: ConfigManager, logger: Logger, daemon: bool = False):
    """Start the monitoring system"""
    logger.info("Starting monitoring system...")
    
    # Validate configuration before starting
    if not validate_configuration(config_manager, logger):
        logger.error("Configuration validation failed. Cannot start monitoring.")
        return
    
    # Validate directories
    monitored_dir = config_manager.get_monitored_directory()
    backup_dir = config_manager.get_backup_directory()
    
    # Create directories if they don't exist
    os.makedirs(monitored_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)
    
    logger.info(f"Monitored directory: {monitored_dir}")
    logger.info(f"Backup directory: {backup_dir}")
    logger.info(f"Detection threshold: {config_manager.get_detection_threshold()} files")
    
    if daemon:
        logger.info("Running in daemon mode")
    
    # Initialize file system monitor (Task 2)
    file_monitor = FileSystemMonitor(logger, monitored_dir)
    
    # Initialize threat detection engine (Task 3)
    threat_detector = ThreatDetector(
        logger=logger,
        detection_threshold=config_manager.get_detection_threshold(),
        time_window_seconds=config_manager.config.get('time_window_seconds', 10),
        suspicious_extensions=config_manager.get_suspicious_extensions()
    )
    
    # Initialize backup manager (Task 4)
    backup_manager = BackupManager(
        backup_directory=backup_dir,
        retention_count=config_manager.config.get('backup_retention', 5)
    )
    
    # Initialize recovery engine (Task 5)
    recovery_engine = RecoveryEngine(backup_manager, logger)
    
    # Initialize automated response system (Task 6)
    automated_response = AutomatedResponseSystem(
        file_monitor=file_monitor,
        threat_detector=threat_detector,
        backup_manager=backup_manager,
        recovery_engine=recovery_engine,
        logger=logger,
        response_threshold=config_manager.config.get('response_threshold', 50)
    )
    
    logger.info("All system components initialized")
    
    # Start file system monitoring
    if not file_monitor.start_monitoring():
        logger.error("Failed to start file system monitoring")
        return
    
    # Start automated response system
    if not automated_response.start_automated_response():
        logger.error("Failed to start automated response system")
        file_monitor.stop_monitoring()
        return
    
    logger.info("Monitoring system started successfully")
    logger.info("System is actively detecting and responding to threats")
    
    # Store references for cleanup
    global _active_systems
    _active_systems = {
        'file_monitor': file_monitor,
        'automated_response': automated_response,
        'logger': logger
    }
    
    if not daemon:
        print("Press Ctrl+C to stop monitoring...")
        try:
            # Real-time monitoring display
            display_real_time_monitoring(automated_response, logger)
        except KeyboardInterrupt:
            logger.info("Shutdown requested")
            stop_monitoring(logger)


# Global reference to active systems for cleanup
_active_systems = {}

def stop_monitoring(logger: Logger):
    """Stop the monitoring system"""
    logger.info("Stopping monitoring system...")
    
    global _active_systems
    
    # Stop automated response system
    if 'automated_response' in _active_systems:
        automated_response = _active_systems['automated_response']
        if automated_response.stop_automated_response():
            logger.info("Automated response system stopped")
        else:
            logger.error("Error stopping automated response system")
    
    # Stop file system monitor
    if 'file_monitor' in _active_systems:
        file_monitor = _active_systems['file_monitor']
        if file_monitor.stop_monitoring():
            logger.info("File system monitoring stopped")
        else:
            logger.error("Error stopping file system monitoring")
    
    logger.info("Monitoring system stopped")
    _active_systems.clear()


def show_status(config_manager: ConfigManager, logger: Logger):
    """Show current system status"""
    logger.info("System Status Check")
    
    config = config_manager.config
    
    print("\n" + "=" * 50)
    print("RANSOMWARE DETECTION TOOL - STATUS")
    print("=" * 50)
    
    # Configuration status
    print(f"Configuration file: {config_manager.config_path}")
    print(f"Monitored directory: {config.get('monitored_directory')}")
    print(f"Backup directory: {config.get('backup_directory')}")
    print(f"Log directory: {config.get('log_directory')}")
    
    # Directory existence check
    monitored_exists = os.path.exists(config.get('monitored_directory', ''))
    backup_exists = os.path.exists(config.get('backup_directory', ''))
    log_exists = os.path.exists(config.get('log_directory', ''))
    
    print(f"Monitored directory exists: {'✓' if monitored_exists else '✗'}")
    print(f"Backup directory exists: {'✓' if backup_exists else '✗'}")
    print(f"Log directory exists: {'✓' if log_exists else '✗'}")
    
    # Detection settings
    print(f"Detection threshold: {config.get('detection_threshold')} files")
    print(f"Time window: {config.get('time_window_seconds')} seconds")
    print(f"Backup retention: {config.get('backup_retention')} versions")
    
    # Suspicious extensions
    extensions = config.get('suspicious_extensions', [])
    print(f"Suspicious extensions: {', '.join(extensions)}")
    
    # TODO: Show monitoring status (Task 2)
    # TODO: Show recent activity (Task 2)
    
    # Show system status
    global _active_systems
    if _active_systems:
        print(f"\nSystem Status:")
        
        # File monitoring status
        if 'file_monitor' in _active_systems:
            file_monitor = _active_systems['file_monitor']
            print(f"  File monitoring: {'Active' if file_monitor.is_active() else 'Inactive'}")
        
        # Automated response status
        if 'automated_response' in _active_systems:
            automated_response = _active_systems['automated_response']
            print(f"  Automated response: {'Active' if automated_response.is_response_active() else 'Inactive'}")
            
            # Show response statistics
            response_stats = automated_response.get_response_statistics()
            print(f"  Response threshold: {response_stats['response_threshold']}")
            print(f"  Threats detected: {response_stats['total_threats_detected']}")
            print(f"  Automatic backups: {response_stats['automatic_backups_created']}")
            print(f"  Automatic recoveries: {response_stats['automatic_recoveries_performed']}")
            print(f"  Response success rate: {response_stats['response_success_rate_percent']}%")
    else:
        print(f"\nSystem Status: Not running")
    
    # Show backup and recovery statistics
    try:
        backup_manager = BackupManager(config.get('backup_directory', './backups'))
        recovery_engine = RecoveryEngine(backup_manager)
        
        backup_stats = backup_manager.get_backup_statistics()
        recovery_stats = recovery_engine.get_recovery_statistics()
        
        print(f"\nBackup Statistics:")
        print(f"  Files backed up: {backup_stats['total_files_backed_up']}")
        print(f"  Total backup versions: {backup_stats['total_backup_versions']}")
        print(f"  Total backup size: {backup_stats['total_backup_size_bytes']} bytes")
        
        print(f"\nRecovery Statistics:")
        print(f"  Recovery attempts: {recovery_stats['total_recovery_attempts']}")
        print(f"  Successful recoveries: {recovery_stats['successful_recoveries']}")
        print(f"  Success rate: {recovery_stats['success_rate_percent']}%")
        
    except Exception as e:
        print(f"Error retrieving statistics: {e}")
    
    print("=" * 50)


def validate_configuration(config_manager: ConfigManager, logger: Logger) -> bool:
    """Validate configuration settings"""
    logger.info("Validating configuration...")
    
    config = config_manager.config
    is_valid = True
    
    # Validate monitored directory
    monitored_dir = config.get('monitored_directory')
    if not monitored_dir:
        logger.error("Monitored directory not specified")
        is_valid = False
    elif not os.path.isabs(monitored_dir) and not monitored_dir.startswith('./'):
        logger.warning(f"Monitored directory '{monitored_dir}' should be absolute or relative path")
    
    # Validate backup directory
    backup_dir = config.get('backup_directory')
    if not backup_dir:
        logger.error("Backup directory not specified")
        is_valid = False
    elif monitored_dir and os.path.abspath(backup_dir) == os.path.abspath(monitored_dir):
        logger.error("Backup directory cannot be the same as monitored directory")
        is_valid = False
    
    # Validate detection threshold
    detection_threshold = config.get('detection_threshold')
    if not isinstance(detection_threshold, int) or detection_threshold < 1:
        logger.error(f"Detection threshold must be a positive integer, got: {detection_threshold}")
        is_valid = False
    elif detection_threshold > 100:
        logger.warning(f"Detection threshold is very high ({detection_threshold}), consider lowering it")
    
    # Validate time window
    time_window = config.get('time_window_seconds')
    if not isinstance(time_window, int) or time_window < 1:
        logger.error(f"Time window must be a positive integer, got: {time_window}")
        is_valid = False
    elif time_window > 300:  # 5 minutes
        logger.warning(f"Time window is very long ({time_window}s), consider shortening it")
    
    # Validate backup retention
    backup_retention = config.get('backup_retention')
    if not isinstance(backup_retention, int) or backup_retention < 1:
        logger.error(f"Backup retention must be a positive integer, got: {backup_retention}")
        is_valid = False
    elif backup_retention > 50:
        logger.warning(f"Backup retention is very high ({backup_retention}), consider lowering it")
    
    # Validate response threshold
    response_threshold = config.get('response_threshold')
    if not isinstance(response_threshold, int) or response_threshold < 0 or response_threshold > 100:
        logger.error(f"Response threshold must be an integer between 0-100, got: {response_threshold}")
        is_valid = False
    
    # Validate suspicious extensions
    suspicious_extensions = config.get('suspicious_extensions')
    if not isinstance(suspicious_extensions, list):
        logger.error("Suspicious extensions must be a list")
        is_valid = False
    elif not suspicious_extensions:
        logger.warning("No suspicious extensions configured")
    else:
        for ext in suspicious_extensions:
            if not isinstance(ext, str) or not ext.startswith('.'):
                logger.error(f"Invalid suspicious extension: {ext} (must start with '.')")
                is_valid = False
    
    # Validate email configuration (if provided)
    alert_email = config.get('alert_email')
    if alert_email and '@' not in alert_email:
        logger.warning(f"Alert email appears invalid: {alert_email}")
    
    if is_valid:
        logger.info("Configuration validation passed")
    else:
        logger.error("Configuration validation failed")
    
    return is_valid


def display_real_time_monitoring(automated_response, logger: Logger):
    """Display real-time monitoring information"""
    import time
    import os
    
    # Clear screen function
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    last_stats = None
    
    while True:
        try:
            # Clear screen for real-time display
            clear_screen()
            
            # Display header
            print("=" * 60)
            print("RANSOMWARE DETECTION TOOL - REAL-TIME MONITORING")
            print("=" * 60)
            print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("Press Ctrl+C to stop monitoring...")
            print("-" * 60)
            
            # Get current statistics
            current_stats = automated_response.get_response_statistics()
            
            # Display monitoring status
            print(f"System Status: {'ACTIVE' if automated_response.is_response_active() else 'INACTIVE'}")
            print(f"Response Threshold: {current_stats['response_threshold']}")
            print()
            
            # Display detection statistics
            print("DETECTION STATISTICS:")
            print(f"  Threats Detected: {current_stats['total_threats_detected']}")
            print(f"  Files Monitored: {current_stats.get('files_monitored', 'N/A')}")
            print(f"  Events Processed: {current_stats.get('events_processed', 'N/A')}")
            print()
            
            # Display response statistics
            print("RESPONSE STATISTICS:")
            print(f"  Automatic Backups: {current_stats['automatic_backups_created']}")
            print(f"  Automatic Recoveries: {current_stats['automatic_recoveries_performed']}")
            print(f"  Success Rate: {current_stats['response_success_rate_percent']}%")
            print()
            
            # Display recent activity (if stats changed)
            if last_stats and current_stats != last_stats:
                print("RECENT ACTIVITY:")
                if current_stats['total_threats_detected'] > last_stats['total_threats_detected']:
                    print(f"  🚨 NEW THREAT DETECTED!")
                if current_stats['automatic_backups_created'] > last_stats['automatic_backups_created']:
                    print(f"  💾 Backup created")
                if current_stats['automatic_recoveries_performed'] > last_stats['automatic_recoveries_performed']:
                    print(f"  🔄 Recovery performed")
                print()
            
            # Display system health
            print("SYSTEM HEALTH:")
            file_monitor = automated_response.file_monitor
            if hasattr(file_monitor, 'is_active') and file_monitor.is_active():
                print(f"  File Monitor: ✓ Active")
            else:
                print(f"  File Monitor: ✗ Inactive")
            
            if automated_response.is_response_active():
                print(f"  Automated Response: ✓ Active")
            else:
                print(f"  Automated Response: ✗ Inactive")
            
            print()
            print("=" * 60)
            
            # Store current stats for next iteration
            last_stats = current_stats.copy()
            
            # Wait before next update
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error in real-time display: {e}")
            time.sleep(1)


def show_config(config_manager: ConfigManager, logger: Logger):
    """Show current configuration"""
    logger.info("Displaying configuration")
    
    print("\n" + "=" * 50)
    print("CURRENT CONFIGURATION")
    print("=" * 50)
    
    import json
    print(json.dumps(config_manager.config, indent=2))
    print("=" * 50)


def validate_config_command(config_manager: ConfigManager, logger: Logger):
    """Validate configuration and display results"""
    logger.info("Running configuration validation")
    
    print("\n" + "=" * 50)
    print("CONFIGURATION VALIDATION")
    print("=" * 50)
    
    is_valid = validate_configuration(config_manager, logger)
    
    if is_valid:
        print("✓ Configuration is valid and ready for use")
        print("  All settings have been validated successfully")
    else:
        print("✗ Configuration has errors that need to be fixed")
        print("  Check the log output above for specific issues")
    
    print("=" * 50)


if __name__ == "__main__":
    main()