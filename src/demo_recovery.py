#!/usr/bin/env python3
"""
Recovery Engine Demonstration Script

This script demonstrates how the RecoveryEngine would be used
in a real ransomware detection and recovery scenario.
"""

import os
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backup_manager import BackupManager
from src.recovery_engine import RecoveryEngine
from src.config_manager import ConfigManager
from src.logger import Logger


def demonstrate_recovery_scenario():
    """Demonstrate a complete ransomware detection and recovery scenario"""
    
    print("=" * 60)
    print("RANSOMWARE RECOVERY DEMONSTRATION")
    print("=" * 60)
    
    # Initialize components
    config_manager = ConfigManager('config.json')
    config = config_manager.load_config()
    
    logger = Logger(
        log_directory=config.get('log_directory', './logs'),
        log_level='INFO'
    )
    
    backup_manager = BackupManager(
        backup_directory=config.get('backup_directory', './backups'),
        retention_count=config.get('backup_retention', 5)
    )
    
    recovery_engine = RecoveryEngine(backup_manager, logger)
    
    # Create test files in monitored directory
    monitored_dir = Path(config.get('monitored_directory', './test_files'))
    monitored_dir.mkdir(exist_ok=True)
    
    test_files = []
    print("\n1. Creating test files...")
    for i in range(3):
        file_path = monitored_dir / f"important_document_{i}.txt"
        content = f"This is important document {i}\nContains critical business data\nCreated: {time.ctime()}"
        file_path.write_text(content)
        test_files.append(str(file_path))
        print(f"   Created: {file_path.name}")
    
    # Create initial backups
    print("\n2. Creating initial backups...")
    for file_path in test_files:
        backup_record = backup_manager.create_backup(file_path)
        if backup_record:
            print(f"   Backed up: {Path(file_path).name}")
        else:
            print(f"   Failed to backup: {Path(file_path).name}")
    
    # Simulate normal file modifications and additional backups
    print("\n3. Simulating normal file activity...")
    time.sleep(1)  # Ensure different timestamps
    for file_path in test_files:
        # Modify file content
        original_content = Path(file_path).read_text()
        modified_content = original_content + f"\nModified at: {time.ctime()}"
        Path(file_path).write_text(modified_content)
        
        # Create another backup
        backup_manager.create_backup(file_path)
        print(f"   Modified and backed up: {Path(file_path).name}")
    
    # Show backup statistics
    print("\n4. Current backup status:")
    backup_stats = backup_manager.get_backup_statistics()
    print(f"   Files backed up: {backup_stats['total_files_backed_up']}")
    print(f"   Total backup versions: {backup_stats['total_backup_versions']}")
    
    # Simulate ransomware attack
    print("\n5. SIMULATING RANSOMWARE ATTACK...")
    print("   Files being encrypted by malicious software...")
    
    for file_path in test_files:
        # Simulate file encryption/corruption
        encrypted_content = "ENCRYPTED_BY_RANSOMWARE_" + "X" * 100
        Path(file_path).write_text(encrypted_content)
        print(f"   ENCRYPTED: {Path(file_path).name}")
    
    print("   RANSOMWARE ATTACK DETECTED!")
    
    # Demonstrate recovery process
    print("\n6. INITIATING AUTOMATED RECOVERY...")
    
    # Recover all affected files
    recovery_results = recovery_engine.restore_multiple(test_files, verify_integrity=True)
    
    print("\n7. Recovery Results:")
    for result in recovery_results:
        file_name = Path(result.file_path).name
        if result.success:
            print(f"   ✓ {file_name}: Successfully restored")
            print(f"     Backup used: {Path(result.backup_used).name}")
            print(f"     Verification: {'Passed' if result.verification_passed else 'Failed'}")
        else:
            print(f"   ✗ {file_name}: Recovery failed - {result.error_message}")
    
    # Show final statistics
    print("\n8. Final Recovery Statistics:")
    recovery_stats = recovery_engine.get_recovery_statistics()
    print(f"   Total recovery attempts: {recovery_stats['total_recovery_attempts']}")
    print(f"   Successful recoveries: {recovery_stats['successful_recoveries']}")
    print(f"   Success rate: {recovery_stats['success_rate_percent']}%")
    
    # Verify file contents were restored
    print("\n9. Verifying restored file contents...")
    for file_path in test_files:
        content = Path(file_path).read_text()
        if "ENCRYPTED_BY_RANSOMWARE" not in content:
            print(f"   ✓ {Path(file_path).name}: Content successfully restored")
        else:
            print(f"   ✗ {Path(file_path).name}: Content still corrupted")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    
    return recovery_stats['success_rate_percent'] == 100.0


if __name__ == "__main__":
    try:
        success = demonstrate_recovery_scenario()
        if success:
            print("\n✓ Recovery demonstration completed successfully!")
        else:
            print("\n✗ Some issues occurred during recovery demonstration.")
    except Exception as e:
        print(f"\nError during demonstration: {e}")