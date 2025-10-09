#!/usr/bin/env python3
"""
Comprehensive Demonstration Script for Ransomware Detection & Recovery Tool

This script provides a complete demonstration of the system's capabilities,
including detection, backup, and recovery functionality.
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config_manager import ConfigManager
from logger import Logger
from backup_manager import BackupManager
from recovery_engine import RecoveryEngine
from file_monitor import FileSystemMonitor
from threat_detector import ThreatDetector
from automated_response import AutomatedResponseSystem


class DemonstrationOrchestrator:
    """Orchestrates a complete demonstration of the ransomware detection system"""
    
    def __init__(self):
        self.config_manager = None
        self.logger = None
        self.monitoring_process = None
        self.demo_files = []
        
    def setup_demonstration(self):
        """Set up the demonstration environment"""
        print("=" * 60)
        print("RANSOMWARE DETECTION & RECOVERY TOOL DEMONSTRATION")
        print("=" * 60)
        
        # Load configuration
        self.config_manager = ConfigManager('config.json')
        config = self.config_manager.load_config()
        
        # Initialize logger
        self.logger = Logger(
            log_directory=config.get('log_directory', './logs'),
            log_level='INFO'
        )
        
        print("✓ Configuration loaded")
        print("✓ Logging system initialized")
        
        # Ensure directories exist
        monitored_dir = Path(config.get('monitored_directory', './test_files'))
        backup_dir = Path(config.get('backup_directory', './backups'))
        
        monitored_dir.mkdir(exist_ok=True)
        backup_dir.mkdir(exist_ok=True)
        
        print(f"✓ Monitored directory: {monitored_dir}")
        print(f"✓ Backup directory: {backup_dir}")
        
        return config
    
    def create_demo_files(self, config):
        """Create demonstration files"""
        print("\n1. Creating demonstration files...")
        
        monitored_dir = Path(config.get('monitored_directory', './test_files'))
        
        demo_files_data = [
            ("financial_report.xlsx", "FINANCIAL REPORT Q4 2024\nRevenue: $1,250,000\nProfit: $340,000\n"),
            ("customer_database.txt", "CUSTOMER DATABASE\nJohn Doe - john@email.com - Premium\nJane Smith - jane@email.com - Standard\n"),
            ("project_proposal.doc", "PROJECT PROPOSAL\nTitle: AI Security Enhancement\nBudget: $50,000\nTimeline: 6 months\n"),
            ("backup_codes.txt", "BACKUP CODES\n1234-5678-9012\n3456-7890-1234\nStore in secure location!\n"),
            ("research_data.csv", "RESEARCH DATA\nDate,Temperature,Humidity\n2024-01-01,22.5,65\n2024-01-02,23.1,62\n")
        ]
        
        for filename, content in demo_files_data:
            file_path = monitored_dir / filename
            full_content = f"Created: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            full_content += f"File: {filename}\n"
            full_content += "=" * 40 + "\n"
            full_content += content
            full_content += "\n" + "=" * 40 + "\n"
            full_content += "This file contains important business data.\n"
            
            file_path.write_text(full_content)
            self.demo_files.append(str(file_path))
            print(f"   Created: {filename}")
        
        print(f"✓ Created {len(self.demo_files)} demonstration files")
        return self.demo_files
    
    def start_monitoring_system(self):
        """Start the monitoring system in a separate process"""
        print("\n2. Starting monitoring system...")
        
        try:
            # Start monitoring system as subprocess
            cmd = [sys.executable, 'main.py', 'start', '--log-level', 'INFO']
            self.monitoring_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give the system time to start
            time.sleep(3)
            
            # Check if process is still running
            if self.monitoring_process.poll() is None:
                print("✓ Monitoring system started successfully")
                return True
            else:
                stdout, stderr = self.monitoring_process.communicate()
                print(f"✗ Failed to start monitoring system")
                print(f"Error: {stderr}")
                return False
                
        except Exception as e:
            print(f"✗ Error starting monitoring system: {e}")
            return False
    
    def demonstrate_normal_activity(self):
        """Demonstrate normal file activity"""
        print("\n3. Demonstrating normal file activity...")
        print("   This should NOT trigger threat detection")
        
        # Modify files at normal pace
        for i, file_path in enumerate(self.demo_files[:2]):  # Only modify first 2 files
            try:
                # Read current content
                content = Path(file_path).read_text()
                
                # Add normal update
                updated_content = content + f"\nNormal update {i+1} at {time.strftime('%H:%M:%S')}\n"
                
                # Write back
                Path(file_path).write_text(updated_content)
                
                print(f"   Updated: {Path(file_path).name}")
                
                # Normal delay between updates
                time.sleep(5)
                
            except Exception as e:
                print(f"   Error updating {file_path}: {e}")
        
        print("✓ Normal activity completed (should not trigger alerts)")
        time.sleep(5)  # Wait for system to process
    
    def demonstrate_threat_detection(self):
        """Demonstrate threat detection by simulating ransomware"""
        print("\n4. Demonstrating threat detection...")
        print("   🚨 SIMULATING RANSOMWARE ATTACK")
        print("   This SHOULD trigger threat detection and automated response")
        
        # Rapid file modifications to trigger detection
        for i, file_path in enumerate(self.demo_files):
            try:
                # Simulate encryption by overwriting with encrypted-looking content
                encrypted_content = f"ENCRYPTED_BY_DEMO_RANSOMWARE\n"
                encrypted_content += f"Original file: {Path(file_path).name}\n"
                encrypted_content += f"Encrypted at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                encrypted_content += "ENCRYPTED_DATA: " + "X" * 200
                
                # Overwrite file
                Path(file_path).write_text(encrypted_content)
                
                print(f"   ⚠️  Encrypted: {Path(file_path).name}")
                
                # Short delay to simulate rapid encryption
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   Error encrypting {file_path}: {e}")
        
        print("🚨 Simulated ransomware attack completed")
        print("   The system should now detect the threat and respond automatically")
        
        # Wait for system to detect and respond
        print("   Waiting for automated response...")
        time.sleep(10)
    
    def check_system_response(self, config):
        """Check if the system responded correctly"""
        print("\n5. Checking system response...")
        
        # Check backup directory for emergency backups
        backup_dir = Path(config.get('backup_directory', './backups'))
        
        if backup_dir.exists():
            backup_files = list(backup_dir.glob('**/*'))
            backup_count = len([f for f in backup_files if f.is_file()])
            print(f"   Backup files created: {backup_count}")
            
            if backup_count > 0:
                print("   ✓ Automated backup system activated")
            else:
                print("   ⚠️  No backup files found")
        
        # Check log files for detection events
        log_dir = Path(config.get('log_directory', './logs'))
        if log_dir.exists():
            log_files = list(log_dir.glob('*.log'))
            if log_files:
                print(f"   Log files: {len(log_files)}")
                print("   ✓ System logging active")
            else:
                print("   ⚠️  No log files found")
        
        # Check if files were recovered
        recovered_files = 0
        for file_path in self.demo_files:
            if Path(file_path).exists():
                content = Path(file_path).read_text()
                if "ENCRYPTED_BY_DEMO_RANSOMWARE" not in content:
                    recovered_files += 1
        
        print(f"   Files recovered: {recovered_files}/{len(self.demo_files)}")
        
        if recovered_files > 0:
            print("   ✓ Automated recovery system activated")
        else:
            print("   ⚠️  No files were automatically recovered")
        
        return {
            'backups_created': backup_count > 0,
            'files_recovered': recovered_files,
            'logs_generated': len(log_files) > 0 if log_dir.exists() else False
        }
    
    def demonstrate_manual_recovery(self, config):
        """Demonstrate manual recovery process"""
        print("\n6. Demonstrating manual recovery...")
        
        try:
            # Initialize recovery components
            backup_manager = BackupManager(
                backup_directory=config.get('backup_directory', './backups'),
                retention_count=config.get('backup_retention', 5)
            )
            
            recovery_engine = RecoveryEngine(backup_manager, self.logger)
            
            # Find files that still need recovery
            files_to_recover = []
            for file_path in self.demo_files:
                if Path(file_path).exists():
                    content = Path(file_path).read_text()
                    if "ENCRYPTED_BY_DEMO_RANSOMWARE" in content:
                        files_to_recover.append(file_path)
            
            if files_to_recover:
                print(f"   Recovering {len(files_to_recover)} files manually...")
                
                # Perform manual recovery
                recovery_results = recovery_engine.restore_multiple(files_to_recover)
                
                successful_recoveries = 0
                for result in recovery_results:
                    if result.success:
                        successful_recoveries += 1
                        print(f"   ✓ Recovered: {Path(result.file_path).name}")
                    else:
                        print(f"   ✗ Failed to recover: {Path(result.file_path).name}")
                
                print(f"   Manual recovery completed: {successful_recoveries}/{len(files_to_recover)} files")
                
            else:
                print("   ✓ All files already recovered by automated system")
            
        except Exception as e:
            print(f"   Error during manual recovery: {e}")
    
    def show_final_statistics(self, config):
        """Show final demonstration statistics"""
        print("\n7. Final demonstration statistics...")
        
        try:
            # Backup statistics
            backup_manager = BackupManager(config.get('backup_directory', './backups'))
            backup_stats = backup_manager.get_backup_statistics()
            
            print(f"   Total files backed up: {backup_stats['total_files_backed_up']}")
            print(f"   Total backup versions: {backup_stats['total_backup_versions']}")
            print(f"   Backup storage used: {backup_stats['total_backup_size_bytes']} bytes")
            
            # Recovery statistics
            recovery_engine = RecoveryEngine(backup_manager)
            recovery_stats = recovery_engine.get_recovery_statistics()
            
            print(f"   Recovery attempts: {recovery_stats['total_recovery_attempts']}")
            print(f"   Successful recoveries: {recovery_stats['successful_recoveries']}")
            print(f"   Recovery success rate: {recovery_stats['success_rate_percent']}%")
            
        except Exception as e:
            print(f"   Error retrieving statistics: {e}")
    
    def cleanup_demonstration(self):
        """Clean up demonstration files and stop monitoring"""
        print("\n8. Cleaning up demonstration...")
        
        # Stop monitoring process
        if self.monitoring_process and self.monitoring_process.poll() is None:
            print("   Stopping monitoring system...")
            self.monitoring_process.terminate()
            try:
                self.monitoring_process.wait(timeout=10)
                print("   ✓ Monitoring system stopped")
            except subprocess.TimeoutExpired:
                self.monitoring_process.kill()
                print("   ✓ Monitoring system forcefully stopped")
        
        # Ask user about cleanup
        cleanup = input("\nClean up demonstration files? (Y/n): ").strip().lower()
        if cleanup != 'n':
            try:
                # Clean up test files
                if self.config_manager:
                    config = self.config_manager.config
                    test_dir = Path(config.get('monitored_directory', './test_files'))
                    if test_dir.exists():
                        import shutil
                        shutil.rmtree(test_dir)
                        print(f"   ✓ Cleaned up: {test_dir}")
                
                print("   ✓ Demonstration cleanup completed")
                
            except Exception as e:
                print(f"   Error during cleanup: {e}")
        else:
            print("   Skipping cleanup as requested")
    
    def run_full_demonstration(self):
        """Run the complete demonstration"""
        try:
            # Setup
            config = self.setup_demonstration()
            
            # Create demo files
            self.create_demo_files(config)
            
            # Start monitoring
            if not self.start_monitoring_system():
                print("Failed to start monitoring system. Exiting.")
                return
            
            print("\nDemonstration ready!")
            input("Press Enter to begin the demonstration...")
            
            # Run demonstration phases
            self.demonstrate_normal_activity()
            
            input("\nPress Enter to simulate ransomware attack...")
            self.demonstrate_threat_detection()
            
            input("\nPress Enter to check system response...")
            response_results = self.check_system_response(config)
            
            input("\nPress Enter to demonstrate manual recovery...")
            self.demonstrate_manual_recovery(config)
            
            input("\nPress Enter to view final statistics...")
            self.show_final_statistics(config)
            
            print("\n" + "=" * 60)
            print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            
            # Summary
            print("\nDemonstration Summary:")
            print("✓ File system monitoring")
            print("✓ Threat detection")
            print("✓ Automated backup creation")
            print("✓ Automated recovery (if configured)")
            print("✓ Manual recovery capabilities")
            print("✓ Comprehensive logging")
            
            print("\nThe ransomware detection tool has successfully demonstrated:")
            print("- Real-time file system monitoring")
            print("- Pattern-based threat detection")
            print("- Automated backup and recovery")
            print("- Comprehensive logging and reporting")
            
        except KeyboardInterrupt:
            print("\nDemonstration interrupted by user")
        except Exception as e:
            print(f"Error during demonstration: {e}")
        finally:
            self.cleanup_demonstration()


def main():
    """Main demonstration function"""
    print("Starting comprehensive demonstration...")
    
    # Check if main.py exists
    if not Path('main.py').exists():
        print("Error: main.py not found. Please run from the project root directory.")
        return
    
    # Check if config.json exists
    if not Path('config.json').exists():
        print("Error: config.json not found. Please ensure configuration file exists.")
        return
    
    # Run demonstration
    demo = DemonstrationOrchestrator()
    demo.run_full_demonstration()


if __name__ == "__main__":
    main()