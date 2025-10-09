"""
Backup Manager Module

This module provides backup functionality for the ransomware detection tool.
It handles creating timestamped backups, verifying backup integrity, and managing
backup retention policies.
"""

import os
import shutil
import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BackupRecord:
    """Data class representing a backup record"""
    original_path: str
    backup_path: str
    timestamp: datetime.datetime
    file_size: int


class BackupManager:
    """
    Manages file backup operations including creation, verification, and cleanup.
    
    This class handles:
    - Creating timestamped backups of files
    - Verifying backup integrity
    - Managing backup retention policies
    - Listing available backups for files
    """
    
    def __init__(self, backup_directory: str, retention_count: int = 5):
        """
        Initialize the BackupManager.
        
        Args:
            backup_directory: Directory where backups will be stored
            retention_count: Number of backup versions to keep per file
        """
        self.backup_directory = Path(backup_directory)
        self.retention_count = retention_count
        self.backup_records: Dict[str, List[BackupRecord]] = {}
        
        # Create backup directory if it doesn't exist
        self.backup_directory.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, file_path: str) -> Optional[BackupRecord]:
        """
        Create a timestamped backup of the specified file.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            BackupRecord if successful, None if failed
        """
        try:
            source_path = Path(file_path)
            
            # Check if source file exists
            if not source_path.exists():
                raise FileNotFoundError(f"Source file does not exist: {file_path}")
            
            # Generate timestamped backup filename
            timestamp = datetime.datetime.now()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Include milliseconds
            
            # Create backup filename: original_name_YYYYMMDD_HHMMSS_mmm.ext
            backup_filename = f"{source_path.stem}_{timestamp_str}{source_path.suffix}"
            backup_path = self.backup_directory / backup_filename
            
            # Copy the file
            shutil.copy2(source_path, backup_path)
            
            # Get file size for verification
            file_size = source_path.stat().st_size
            
            # Create backup record
            backup_record = BackupRecord(
                original_path=str(source_path.absolute()),
                backup_path=str(backup_path.absolute()),
                timestamp=timestamp,
                file_size=file_size
            )
            
            # Store backup record
            original_key = str(source_path.absolute())
            if original_key not in self.backup_records:
                self.backup_records[original_key] = []
            
            self.backup_records[original_key].append(backup_record)
            
            # Clean up old backups if retention limit exceeded
            self._cleanup_old_backups(original_key)
            
            return backup_record
            
        except Exception as e:
            # Log error but don't raise to prevent system crash
            print(f"Error creating backup for {file_path}: {e}")
            return None
    
    def verify_backup(self, backup_path: str) -> bool:
        """
        Verify that a backup file exists and has the expected size.
        
        Args:
            backup_path: Path to the backup file to verify
            
        Returns:
            True if backup is valid, False otherwise
        """
        try:
            backup_file = Path(backup_path)
            
            # Check if backup file exists
            if not backup_file.exists():
                return False
            
            # Find the corresponding backup record
            for records in self.backup_records.values():
                for record in records:
                    if record.backup_path == backup_path:
                        # Verify file size matches
                        actual_size = backup_file.stat().st_size
                        return actual_size == record.file_size
            
            # If no record found, just check if file exists and has size > 0
            return backup_file.stat().st_size > 0
            
        except Exception as e:
            print(f"Error verifying backup {backup_path}: {e}")
            return False
    
    def list_backups(self, original_file: str) -> List[BackupRecord]:
        """
        List all available backup versions for a specific file.
        
        Args:
            original_file: Path to the original file
            
        Returns:
            List of BackupRecord objects, sorted by timestamp (newest first)
        """
        original_key = str(Path(original_file).absolute())
        
        if original_key in self.backup_records:
            # Sort by timestamp, newest first
            return sorted(
                self.backup_records[original_key],
                key=lambda x: x.timestamp,
                reverse=True
            )
        
        return []
    
    def get_latest_backup(self, original_file: str) -> Optional[BackupRecord]:
        """
        Get the most recent backup for a specific file.
        
        Args:
            original_file: Path to the original file
            
        Returns:
            Most recent BackupRecord or None if no backups exist
        """
        backups = self.list_backups(original_file)
        return backups[0] if backups else None
    
    def cleanup_old_backups(self) -> int:
        """
        Clean up old backups for all files based on retention policy.
        
        Returns:
            Number of backup files removed
        """
        removed_count = 0
        
        for original_file in list(self.backup_records.keys()):
            removed_count += self._cleanup_old_backups(original_file)
        
        return removed_count
    
    def _cleanup_old_backups(self, original_file: str) -> int:
        """
        Clean up old backups for a specific file.
        
        Args:
            original_file: Key for the original file
            
        Returns:
            Number of backup files removed
        """
        if original_file not in self.backup_records:
            return 0
        
        records = self.backup_records[original_file]
        
        # Sort by timestamp, newest first
        records.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Keep only the most recent backups up to retention limit
        if len(records) <= self.retention_count:
            return 0
        
        # Remove excess backups
        excess_records = records[self.retention_count:]
        removed_count = 0
        
        for record in excess_records:
            try:
                backup_path = Path(record.backup_path)
                if backup_path.exists():
                    backup_path.unlink()
                    removed_count += 1
            except Exception as e:
                print(f"Error removing old backup {record.backup_path}: {e}")
        
        # Update records list
        self.backup_records[original_file] = records[:self.retention_count]
        
        return removed_count
    
    def get_backup_statistics(self) -> Dict[str, int]:
        """
        Get statistics about current backups.
        
        Returns:
            Dictionary with backup statistics
        """
        total_files = len(self.backup_records)
        total_backups = sum(len(records) for records in self.backup_records.values())
        
        # Calculate total backup size
        total_size = 0
        for records in self.backup_records.values():
            for record in records:
                try:
                    backup_path = Path(record.backup_path)
                    if backup_path.exists():
                        total_size += backup_path.stat().st_size
                except Exception:
                    pass
        
        return {
            'total_files_backed_up': total_files,
            'total_backup_versions': total_backups,
            'total_backup_size_bytes': total_size,
            'backup_directory': str(self.backup_directory),
            'retention_count': self.retention_count
        }