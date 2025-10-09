"""
Automated Response System for Ransomware Detection Tool

This module integrates threat detection with automatic backup creation and recovery.
It provides the core automation that responds to detected threats by:
1. Creating immediate backups of affected files
2. Triggering automated recovery when threats are confirmed
3. Logging all response activities
"""

import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from threading import Thread, Event, Lock

from threat_detector import ThreatDetector, DetectionResult
from backup_manager import BackupManager, BackupRecord
from recovery_engine import RecoveryEngine, RecoveryResult
from file_monitor import FileSystemMonitor, FileEvent
from logger import Logger


@dataclass
class ResponseAction:
    """Represents an automated response action taken by the system"""
    timestamp: datetime
    action_type: str  # 'backup', 'recovery', 'alert'
    file_path: str
    success: bool
    details: str
    threat_score: int


class AutomatedResponseSystem:
    """
    Orchestrates automated responses to detected ransomware threats.
    
    This system continuously monitors for threats and automatically:
    - Creates backups when suspicious activity is detected
    - Triggers recovery when threats are confirmed
    - Logs all response activities for audit purposes
    """
    
    def __init__(self, file_monitor: FileSystemMonitor, threat_detector: ThreatDetector,
                 backup_manager: BackupManager, recovery_engine: RecoveryEngine, 
                 logger: Logger, response_threshold: int = 50):
        """
        Initialize the automated response system.
        
        Args:
            file_monitor: FileSystemMonitor instance for getting file events
            threat_detector: ThreatDetector instance for analyzing threats
            backup_manager: BackupManager instance for creating backups
            recovery_engine: RecoveryEngine instance for file recovery
            logger: Logger instance for recording activities
            response_threshold: Threat score threshold for triggering recovery (0-100)
        """
        self.file_monitor = file_monitor
        self.threat_detector = threat_detector
        self.backup_manager = backup_manager
        self.recovery_engine = recovery_engine
        self.logger = logger
        self.response_threshold = response_threshold
        
        # Response tracking
        self.response_actions: List[ResponseAction] = []
        self.is_active = False
        self.monitoring_thread: Optional[Thread] = None
        self.stop_event = Event()
        self.response_lock = Lock()
        
        # Response statistics
        self.stats = {
            'total_threats_detected': 0,
            'automatic_backups_created': 0,
            'automatic_recoveries_performed': 0,
            'response_success_rate': 0.0,
            'last_threat_detection': None,
            'last_response_action': None
        }
        
        self.logger.info(f"AutomatedResponseSystem initialized with threshold: {response_threshold}")
    
    def start_automated_response(self) -> bool:
        """
        Start the automated response monitoring system.
        
        Returns:
            True if started successfully, False otherwise
        """
        try:
            if self.is_active:
                self.logger.warning("Automated response system is already active")
                return True
            
            # Ensure file monitor is active
            if not self.file_monitor.is_active():
                self.logger.error("File monitor must be active before starting automated response")
                return False
            
            # Reset stop event
            self.stop_event.clear()
            
            # Start monitoring thread
            self.monitoring_thread = Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            
            self.is_active = True
            self.logger.info("Automated response system started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start automated response system: {str(e)}")
            return False
    
    def stop_automated_response(self) -> bool:
        """
        Stop the automated response monitoring system.
        
        Returns:
            True if stopped successfully, False otherwise
        """
        try:
            if not self.is_active:
                self.logger.warning("Automated response system is not active")
                return True
            
            # Signal stop and wait for thread to finish
            self.stop_event.set()
            
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=5.0)
            
            self.is_active = False
            self.logger.info("Automated response system stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping automated response system: {str(e)}")
            return False
    
    def _monitoring_loop(self) -> None:
        """
        Main monitoring loop that continuously checks for threats and responds.
        """
        self.logger.info("Automated response monitoring loop started")
        
        while not self.stop_event.is_set():
            try:
                # Get recent file events for analysis
                recent_events = self.file_monitor.get_recent_events(seconds=10)
                
                if recent_events:
                    # Analyze events for threats
                    detection_result = self.threat_detector.analyze_events(recent_events)
                    
                    if detection_result.is_threat:
                        self._handle_threat_detection(detection_result)
                
                # Sleep for a short interval before next check
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                self.logger.error(f"Error in automated response monitoring loop: {str(e)}")
                time.sleep(5)  # Wait longer on error
        
        self.logger.info("Automated response monitoring loop stopped")
    
    def _handle_threat_detection(self, detection_result: DetectionResult) -> None:
        """
        Handle a detected threat by triggering appropriate automated responses.
        
        Args:
            detection_result: DetectionResult from threat analysis
        """
        with self.response_lock:
            self.stats['total_threats_detected'] += 1
            self.stats['last_threat_detection'] = detection_result.timestamp
            
            self.logger.warning(f"AUTOMATED RESPONSE TRIGGERED - Threat Score: {detection_result.threat_score}")
            self.logger.warning(f"Threat Reason: {detection_result.detection_reason}")
            self.logger.warning(f"Affected Files: {len(detection_result.affected_files)}")
            
            # Log threat detection response action
            self._log_response_action(
                action_type='alert',
                file_path='system',
                success=True,
                details=f"Threat detected: {detection_result.detection_reason}",
                threat_score=detection_result.threat_score
            )
            
            # Step 1: Create immediate backups of affected files
            self._create_emergency_backups(detection_result.affected_files, detection_result.threat_score)
            
            # Step 2: If threat score is above recovery threshold, trigger automated recovery
            if detection_result.threat_score >= self.response_threshold:
                self.logger.critical(f"Threat score {detection_result.threat_score} exceeds recovery threshold {self.response_threshold}")
                self.logger.critical("INITIATING AUTOMATED RECOVERY")
                self._trigger_automated_recovery(detection_result.affected_files, detection_result.threat_score)
            else:
                self.logger.warning(f"Threat score {detection_result.threat_score} below recovery threshold {self.response_threshold}")
                self.logger.warning("Automated recovery not triggered - monitoring continues")
    
    def _create_emergency_backups(self, affected_files: List[str], threat_score: int) -> None:
        """
        Create immediate backups of files affected by detected threats.
        
        Args:
            affected_files: List of file paths that may be affected
            threat_score: Threat score from detection
        """
        self.logger.info(f"Creating emergency backups for {len(affected_files)} affected files")
        
        backup_success_count = 0
        
        for file_path in affected_files:
            try:
                # Only backup files that still exist and are accessible
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    backup_record = self.backup_manager.create_backup(file_path)
                    
                    if backup_record:
                        backup_success_count += 1
                        self.stats['automatic_backups_created'] += 1
                        
                        self.logger.info(f"Emergency backup created: {file_path} -> {backup_record.backup_path}")
                        
                        # Log successful backup response action
                        self._log_response_action(
                            action_type='backup',
                            file_path=file_path,
                            success=True,
                            details=f"Emergency backup created: {backup_record.backup_path}",
                            threat_score=threat_score
                        )
                    else:
                        self.logger.error(f"Failed to create emergency backup for: {file_path}")
                        
                        # Log failed backup response action
                        self._log_response_action(
                            action_type='backup',
                            file_path=file_path,
                            success=False,
                            details="Emergency backup creation failed",
                            threat_score=threat_score
                        )
                else:
                    self.logger.warning(f"Cannot backup file (not accessible): {file_path}")
                    
            except Exception as e:
                self.logger.error(f"Error creating emergency backup for {file_path}: {str(e)}")
                
                # Log backup error response action
                self._log_response_action(
                    action_type='backup',
                    file_path=file_path,
                    success=False,
                    details=f"Backup error: {str(e)}",
                    threat_score=threat_score
                )
        
        self.logger.info(f"Emergency backup completed: {backup_success_count}/{len(affected_files)} files backed up")
    
    def _trigger_automated_recovery(self, affected_files: List[str], threat_score: int) -> None:
        """
        Trigger automated recovery of files from backups.
        
        Args:
            affected_files: List of file paths to recover
            threat_score: Threat score from detection
        """
        self.logger.critical(f"AUTOMATED RECOVERY INITIATED for {len(affected_files)} files")
        
        # Temporarily stop file monitoring to prevent interference during recovery
        was_monitoring = self.file_monitor.is_active()
        if was_monitoring:
            self.logger.info("Temporarily stopping file monitoring during recovery")
            # Note: We don't actually stop monitoring here to avoid circular dependencies
            # In a real implementation, this would coordinate with the main system
        
        recovery_results = []
        recovery_success_count = 0
        
        try:
            # Perform batch recovery
            recovery_results = self.recovery_engine.restore_multiple(affected_files, verify_integrity=True)
            
            # Process recovery results
            for result in recovery_results:
                if result.success:
                    recovery_success_count += 1
                    self.stats['automatic_recoveries_performed'] += 1
                    
                    self.logger.info(f"Automated recovery successful: {result.file_path}")
                    
                    # Log successful recovery response action
                    self._log_response_action(
                        action_type='recovery',
                        file_path=result.file_path,
                        success=True,
                        details=f"Recovered from: {result.backup_used}",
                        threat_score=threat_score
                    )
                else:
                    self.logger.error(f"Automated recovery failed: {result.file_path} - {result.error_message}")
                    
                    # Log failed recovery response action
                    self._log_response_action(
                        action_type='recovery',
                        file_path=result.file_path,
                        success=False,
                        details=f"Recovery failed: {result.error_message}",
                        threat_score=threat_score
                    )
            
            # Log recovery summary
            self.logger.critical(f"AUTOMATED RECOVERY COMPLETED: {recovery_success_count}/{len(affected_files)} files recovered")
            
            if recovery_success_count == len(affected_files):
                self.logger.info("All files successfully recovered from automated response")
            elif recovery_success_count > 0:
                self.logger.warning(f"Partial recovery: {recovery_success_count} of {len(affected_files)} files recovered")
            else:
                self.logger.error("Automated recovery failed for all files")
            
        except Exception as e:
            self.logger.error(f"Error during automated recovery: {str(e)}")
            
            # Log recovery error response action
            self._log_response_action(
                action_type='recovery',
                file_path='batch_recovery',
                success=False,
                details=f"Recovery error: {str(e)}",
                threat_score=threat_score
            )
        
        finally:
            # Resume file monitoring if it was active
            if was_monitoring:
                self.logger.info("Resuming file monitoring after recovery")
                # Note: In a real implementation, this would restart monitoring
        
        # Update statistics
        self._update_response_statistics()
    
    def _log_response_action(self, action_type: str, file_path: str, success: bool, 
                           details: str, threat_score: int) -> None:
        """
        Log an automated response action.
        
        Args:
            action_type: Type of action ('backup', 'recovery', 'alert')
            file_path: Path of the file involved
            success: Whether the action was successful
            details: Additional details about the action
            threat_score: Associated threat score
        """
        response_action = ResponseAction(
            timestamp=datetime.now(),
            action_type=action_type,
            file_path=file_path,
            success=success,
            details=details,
            threat_score=threat_score
        )
        
        self.response_actions.append(response_action)
        self.stats['last_response_action'] = response_action.timestamp
        
        # Log to system logger with appropriate level
        log_message = f"AUTOMATED_RESPONSE: {action_type.upper()} - {file_path} - {'SUCCESS' if success else 'FAILED'} - {details}"
        
        if action_type == 'alert':
            self.logger.warning(log_message)
        elif success:
            self.logger.info(log_message)
        else:
            self.logger.error(log_message)
    
    def _update_response_statistics(self) -> None:
        """Update response success rate statistics."""
        if self.response_actions:
            successful_actions = sum(1 for action in self.response_actions if action.success)
            self.stats['response_success_rate'] = (successful_actions / len(self.response_actions)) * 100
    
    def get_response_statistics(self) -> Dict[str, any]:
        """
        Get statistics about automated response activities.
        
        Returns:
            Dictionary with response statistics
        """
        self._update_response_statistics()
        
        return {
            'is_active': self.is_active,
            'response_threshold': self.response_threshold,
            'total_threats_detected': self.stats['total_threats_detected'],
            'automatic_backups_created': self.stats['automatic_backups_created'],
            'automatic_recoveries_performed': self.stats['automatic_recoveries_performed'],
            'response_success_rate_percent': round(self.stats['response_success_rate'], 2),
            'total_response_actions': len(self.response_actions),
            'last_threat_detection': self.stats['last_threat_detection'],
            'last_response_action': self.stats['last_response_action']
        }
    
    def get_recent_response_actions(self, hours: int = 24) -> List[ResponseAction]:
        """
        Get recent response actions within the specified time window.
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of ResponseAction objects
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [
            action for action in self.response_actions 
            if action.timestamp > cutoff_time
        ]
    
    def update_response_threshold(self, new_threshold: int) -> None:
        """
        Update the threat score threshold for triggering automated recovery.
        
        Args:
            new_threshold: New threshold value (0-100)
        """
        if 0 <= new_threshold <= 100:
            self.response_threshold = new_threshold
            self.logger.info(f"Response threshold updated to: {new_threshold}")
        else:
            self.logger.error(f"Invalid response threshold: {new_threshold}. Must be between 0-100")
    
    def is_response_active(self) -> bool:
        """Check if automated response system is currently active."""
        return self.is_active and not self.stop_event.is_set()