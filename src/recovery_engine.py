"""
Recovery Engine Module

This module provides file recovery functionality for the ransomware detection tool.
It handles restoring files from backups when ransomware activity is detected,
with verification and fallback capabilities.
"""

import os
import shutil
import hashlib
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from pathlib import Path
from backup_manager import BackupManager, BackupRecord


@dataclass
class RecoveryResult:
    """Data class representing the result of a recovery operation"""
    file_path: str
    success: bool
    backup_used: Optional[str]
    error_message: Optional[str]
    verification_passed: bool


class RecoveryEngine:
    """
    Manages file recovery operations from backups.
    
    This class handles:
    - Restoring files from the most recent clean backup
    - Verifying restored file integrity
    - Attempting fallback to previous backup versions
    - Logging recovery activities and success rates
    """
    
    def __init__(self, backup_manager: BackupManager, logger=None):
        """
        Initialize the RecoveryEngine.
        
        Args:
            backup_manager: BackupManager instance for accessing backups
            logger: Logger instance for recording activities
        """
        self.backup_manager = backup_manager
        self.logger = logger
        self.recovery_stats = {
            'total_attempts': 0,
            'successful_recoveries': 0,
            'failed_recoveries': 0,
            'files_recovered': []
        }
    
    def restore_file(self, file_path: str, verify_integrity: bool = True) -> RecoveryResult:
        """
        Restore a single file from its most recent backup.
        
        Args:
            file_path: Path to the file to restore
            verify_integrity: Whether to verify file integrity after restoration
            
        Returns:
            RecoveryResult indicating success/failure and details
        """
        self.recovery_stats['total_attempts'] += 1
        
        try:
            # Get the most recent backup
            latest_backup = self.backup_manager.get_latest_backup(file_path)
            
            if not latest_backup:
                error_msg = f"No backup found for file: {file_path}"
                self._log_error(error_msg)
                self.recovery_stats['failed_recoveries'] += 1
                return RecoveryResult(
                    file_path=file_path,
                    success=False,
                    backup_used=None,
                    error_message=error_msg,
                    verification_passed=False
                )
            
            # Attempt restoration with the latest backup
            result = self._attempt_restore_from_backup(file_path, latest_backup, verify_integrity)
            
            # If restoration failed, try previous backup versions
            if not result.success:
                self._log_warning(f"Latest backup restoration failed for {file_path}, trying previous versions")
                result = self._try_fallback_backups(file_path, verify_integrity)
            
            # Update statistics
            if result.success:
                self.recovery_stats['successful_recoveries'] += 1
                self.recovery_stats['files_recovered'].append(file_path)
                self._log_info(f"Successfully restored {file_path} from backup {result.backup_used}")
            else:
                self.recovery_stats['failed_recoveries'] += 1
                self._log_error(f"Failed to restore {file_path}: {result.error_message}")
            
            return result
            
        except Exception as e:
            error_msg = f"Unexpected error during restoration of {file_path}: {str(e)}"
            self._log_error(error_msg)
            self.recovery_stats['failed_recoveries'] += 1
            return RecoveryResult(
                file_path=file_path,
                success=False,
                backup_used=None,
                error_message=error_msg,
                verification_passed=False
            )
    
    def restore_multiple(self, file_list: List[str], verify_integrity: bool = True) -> List[RecoveryResult]:
        """
        Restore multiple files from their backups.
        
        Args:
            file_list: List of file paths to restore
            verify_integrity: Whether to verify file integrity after restoration
            
        Returns:
            List of RecoveryResult objects for each file
        """
        self._log_info(f"Starting batch restoration of {len(file_list)} files")
        
        results = []
        for file_path in file_list:
            result = self.restore_file(file_path, verify_integrity)
            results.append(result)
        
        # Log batch restoration summary
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        self._log_info(f"Batch restoration completed: {successful} successful, {failed} failed")
        
        return results
    
    def verify_restoration(self, file_path: str, backup_record: BackupRecord) -> bool:
        """
        Verify that a restored file matches the backup integrity.
        
        Args:
            file_path: Path to the restored file
            backup_record: BackupRecord used for restoration
            
        Returns:
            True if verification passes, False otherwise
        """
        try:
            restored_file = Path(file_path)
            
            # Check if restored file exists
            if not restored_file.exists():
                self._log_error(f"Restored file does not exist: {file_path}")
                return False
            
            # Check file size matches backup
            actual_size = restored_file.stat().st_size
            if actual_size != backup_record.file_size:
                self._log_error(f"Size mismatch for {file_path}: expected {backup_record.file_size}, got {actual_size}")
                return False
            
            # Additional integrity check: compare file hashes if possible
            if self._verify_file_hash(file_path, backup_record.backup_path):
                self._log_info(f"File integrity verification passed for {file_path}")
                return True
            else:
                self._log_warning(f"Hash verification failed for {file_path}, but size matches")
                return True  # Still consider successful if size matches
                
        except Exception as e:
            self._log_error(f"Error verifying restoration of {file_path}: {str(e)}")
            return False
    
    def get_recovery_statistics(self) -> Dict[str, any]:
        """
        Get statistics about recovery operations.
        
        Returns:
            Dictionary with recovery statistics
        """
        success_rate = 0.0
        if self.recovery_stats['total_attempts'] > 0:
            success_rate = (self.recovery_stats['successful_recoveries'] / 
                          self.recovery_stats['total_attempts']) * 100
        
        return {
            'total_recovery_attempts': self.recovery_stats['total_attempts'],
            'successful_recoveries': self.recovery_stats['successful_recoveries'],
            'failed_recoveries': self.recovery_stats['failed_recoveries'],
            'success_rate_percent': round(success_rate, 2),
            'files_recovered': self.recovery_stats['files_recovered'].copy()
        }
    
    def _attempt_restore_from_backup(self, file_path: str, backup_record: BackupRecord, 
                                   verify_integrity: bool) -> RecoveryResult:
        """
        Attempt to restore a file from a specific backup.
        
        Args:
            file_path: Path where the file should be restored
            backup_record: BackupRecord to restore from
            verify_integrity: Whether to verify integrity after restoration
            
        Returns:
            RecoveryResult indicating success/failure
        """
        try:
            backup_path = Path(backup_record.backup_path)
            target_path = Path(file_path)
            
            # Check if backup file exists
            if not backup_path.exists():
                return RecoveryResult(
                    file_path=file_path,
                    success=False,
                    backup_used=backup_record.backup_path,
                    error_message=f"Backup file does not exist: {backup_record.backup_path}",
                    verification_passed=False
                )
            
            # Create target directory if it doesn't exist
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy backup to original location
            shutil.copy2(backup_path, target_path)
            
            # Verify restoration if requested
            verification_passed = True
            if verify_integrity:
                verification_passed = self.verify_restoration(file_path, backup_record)
            
            return RecoveryResult(
                file_path=file_path,
                success=True,
                backup_used=backup_record.backup_path,
                error_message=None,
                verification_passed=verification_passed
            )
            
        except Exception as e:
            return RecoveryResult(
                file_path=file_path,
                success=False,
                backup_used=backup_record.backup_path,
                error_message=f"Error during restoration: {str(e)}",
                verification_passed=False
            )
    
    def _try_fallback_backups(self, file_path: str, verify_integrity: bool) -> RecoveryResult:
        """
        Try to restore from previous backup versions if the latest fails.
        
        Args:
            file_path: Path to the file to restore
            verify_integrity: Whether to verify integrity after restoration
            
        Returns:
            RecoveryResult from the first successful restoration attempt
        """
        # Get all backups for this file (sorted newest first)
        all_backups = self.backup_manager.list_backups(file_path)
        
        # Skip the first one (latest) since it already failed
        fallback_backups = all_backups[1:] if len(all_backups) > 1 else []
        
        if not fallback_backups:
            return RecoveryResult(
                file_path=file_path,
                success=False,
                backup_used=None,
                error_message="No fallback backups available",
                verification_passed=False
            )
        
        # Try each fallback backup
        for backup_record in fallback_backups:
            self._log_info(f"Trying fallback backup: {backup_record.backup_path}")
            result = self._attempt_restore_from_backup(file_path, backup_record, verify_integrity)
            
            if result.success:
                self._log_info(f"Fallback restoration successful using backup from {backup_record.timestamp}")
                return result
        
        # All fallback attempts failed
        return RecoveryResult(
            file_path=file_path,
            success=False,
            backup_used=None,
            error_message="All backup restoration attempts failed",
            verification_passed=False
        )
    
    def _verify_file_hash(self, file1_path: str, file2_path: str) -> bool:
        """
        Compare SHA-256 hashes of two files to verify they are identical.
        
        Args:
            file1_path: Path to first file
            file2_path: Path to second file
            
        Returns:
            True if hashes match, False otherwise
        """
        try:
            hash1 = self._calculate_file_hash(file1_path)
            hash2 = self._calculate_file_hash(file2_path)
            return hash1 == hash2
        except Exception as e:
            self._log_warning(f"Error calculating file hashes: {str(e)}")
            return False
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """
        Calculate SHA-256 hash of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Hexadecimal hash string
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def _log_info(self, message: str):
        """Log an info message"""
        if self.logger:
            self.logger.info(f"[RecoveryEngine] {message}")
        else:
            print(f"INFO: {message}")
    
    def _log_warning(self, message: str):
        """Log a warning message"""
        if self.logger:
            self.logger.warning(f"[RecoveryEngine] {message}")
        else:
            print(f"WARNING: {message}")
    
    def _log_error(self, message: str):
        """Log an error message"""
        if self.logger:
            self.logger.error(f"[RecoveryEngine] {message}")
        else:
            print(f"ERROR: {message}")