"""
Threat Detection Engine for Ransomware Detection Tool
Implements simple pattern-based ransomware detection
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass

from .logger import Logger
from .file_monitor import FileEvent


@dataclass
class DetectionResult:
    """Represents the result of threat detection analysis"""
    is_threat: bool
    threat_score: int  # 0-100
    affected_files: List[str]
    detection_reason: str
    timestamp: datetime


class ThreatDetector:
    """
    Simple threat detection engine that analyzes file system events
    for patterns indicative of ransomware activity
    """
    
    def __init__(self, logger: Logger, detection_threshold: int = 5, 
                 time_window_seconds: int = 10, suspicious_extensions: List[str] = None):
        self.logger = logger
        self.detection_threshold = detection_threshold
        self.time_window_seconds = time_window_seconds
        self.suspicious_extensions = suspicious_extensions or [
            ".encrypted", ".locked", ".crypto", ".crypt", ".enc", ".vault"
        ]
        
        # Convert extensions to lowercase for case-insensitive matching
        self.suspicious_extensions = [ext.lower() for ext in self.suspicious_extensions]
        
        self.logger.info(f"ThreatDetector initialized with threshold: {detection_threshold}, "
                        f"time window: {time_window_seconds}s")
        self.logger.info(f"Monitoring for suspicious extensions: {self.suspicious_extensions}")
    
    def analyze_events(self, events: List[FileEvent]) -> DetectionResult:
        """
        Analyze a list of file events for ransomware patterns
        
        Args:
            events: List of FileEvent objects to analyze
            
        Returns:
            DetectionResult with threat assessment
        """
        try:
            # Filter events to the specified time window
            recent_events = self._filter_recent_events(events)
            
            if not recent_events:
                return DetectionResult(
                    is_threat=False,
                    threat_score=0,
                    affected_files=[],
                    detection_reason="No recent file activity",
                    timestamp=datetime.now()
                )
            
            # Calculate threat score based on multiple factors
            threat_score = 0
            detection_reasons = []
            affected_files = []
            
            # Check file modification rate
            modification_score, mod_files = self._check_modification_rate(recent_events)
            threat_score += modification_score
            affected_files.extend(mod_files)
            if modification_score > 0:
                detection_reasons.append(f"High modification rate: {len(mod_files)} files in {self.time_window_seconds}s")
            
            # Check for suspicious file extensions
            extension_score, ext_files = self._check_suspicious_extensions(recent_events)
            threat_score += extension_score
            affected_files.extend(ext_files)
            if extension_score > 0:
                detection_reasons.append(f"Suspicious file extensions detected: {len(ext_files)} files")
            
            # Check for rapid file size changes (potential encryption)
            size_score, size_files = self._check_file_size_changes(recent_events)
            threat_score += size_score
            affected_files.extend(size_files)
            if size_score > 0:
                detection_reasons.append(f"Rapid file size changes: {len(size_files)} files")
            
            # Remove duplicates from affected files
            affected_files = list(set(affected_files))
            
            # Determine if this constitutes a threat
            is_threat = threat_score >= 50  # Threat threshold of 50/100
            
            detection_reason = "; ".join(detection_reasons) if detection_reasons else "No threats detected"
            
            result = DetectionResult(
                is_threat=is_threat,
                threat_score=min(threat_score, 100),  # Cap at 100
                affected_files=affected_files,
                detection_reason=detection_reason,
                timestamp=datetime.now()
            )
            
            # Log the detection result
            if is_threat:
                self.logger.warning(f"THREAT DETECTED - Score: {result.threat_score}/100, "
                                  f"Reason: {result.detection_reason}")
                self.logger.warning(f"Affected files: {len(affected_files)}")
            else:
                self.logger.debug(f"No threat detected - Score: {result.threat_score}/100")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error during threat analysis: {str(e)}")
            return DetectionResult(
                is_threat=False,
                threat_score=0,
                affected_files=[],
                detection_reason=f"Analysis error: {str(e)}",
                timestamp=datetime.now()
            )
    
    def _filter_recent_events(self, events: List[FileEvent]) -> List[FileEvent]:
        """Filter events to only include those within the time window"""
        cutoff_time = datetime.now() - timedelta(seconds=self.time_window_seconds)
        return [event for event in events if event.timestamp > cutoff_time]
    
    def _check_modification_rate(self, events: List[FileEvent]) -> tuple[int, List[str]]:
        """
        Check if file modification rate exceeds threshold
        
        Returns:
            tuple: (threat_score, list_of_affected_files)
        """
        # Count modifications and creations (both indicate file activity)
        modification_events = [
            event for event in events 
            if event.event_type in ['modified', 'created']
        ]
        
        modification_count = len(modification_events)
        affected_files = [event.file_path for event in modification_events]
        
        if modification_count >= self.detection_threshold:
            # Score based on how much the threshold is exceeded
            excess = modification_count - self.detection_threshold
            score = min(30 + (excess * 5), 50)  # Base 30 points, +5 per excess file, max 50
            return score, affected_files
        
        return 0, []
    
    def _check_suspicious_extensions(self, events: List[FileEvent]) -> tuple[int, List[str]]:
        """
        Check for files with suspicious extensions that might indicate encryption
        
        Returns:
            tuple: (threat_score, list_of_affected_files)
        """
        suspicious_files = []
        
        for event in events:
            if event.event_type in ['modified', 'created']:
                file_path = event.file_path.lower()
                
                # Check if file has suspicious extension
                for ext in self.suspicious_extensions:
                    if file_path.endswith(ext):
                        suspicious_files.append(event.file_path)
                        break
        
        if suspicious_files:
            # High score for suspicious extensions (strong indicator)
            score = min(40 + (len(suspicious_files) * 10), 60)  # Base 40, +10 per file, max 60
            return score, suspicious_files
        
        return 0, []
    
    def _check_file_size_changes(self, events: List[FileEvent]) -> tuple[int, List[str]]:
        """
        Check for rapid file size changes that might indicate encryption
        
        Returns:
            tuple: (threat_score, list_of_affected_files)
        """
        # Group events by file path to track size changes
        file_events: Dict[str, List[FileEvent]] = {}
        
        for event in events:
            if event.event_type == 'modified':
                if event.file_path not in file_events:
                    file_events[event.file_path] = []
                file_events[event.file_path].append(event)
        
        suspicious_files = []
        
        for file_path, file_event_list in file_events.items():
            if len(file_event_list) >= 2:  # Need at least 2 events to compare sizes
                # Sort by timestamp
                file_event_list.sort(key=lambda x: x.timestamp)
                
                # Check for significant size increases (potential encryption overhead)
                for i in range(1, len(file_event_list)):
                    prev_size = file_event_list[i-1].file_size
                    curr_size = file_event_list[i].file_size
                    
                    if prev_size > 0 and curr_size > prev_size:
                        size_increase_ratio = curr_size / prev_size
                        
                        # If file size increased by more than 20%, it's suspicious
                        if size_increase_ratio > 1.2:
                            suspicious_files.append(file_path)
                            break
        
        if suspicious_files:
            # Moderate score for size changes
            score = min(20 + (len(suspicious_files) * 5), 30)  # Base 20, +5 per file, max 30
            return score, suspicious_files
        
        return 0, []
    
    def is_suspicious_extension(self, filename: str) -> bool:
        """
        Check if a filename has a suspicious extension
        
        Args:
            filename: Name of the file to check
            
        Returns:
            bool: True if extension is suspicious
        """
        filename_lower = filename.lower()
        return any(filename_lower.endswith(ext) for ext in self.suspicious_extensions)
    
    def update_detection_threshold(self, new_threshold: int) -> None:
        """Update the detection threshold"""
        self.detection_threshold = new_threshold
        self.logger.info(f"Detection threshold updated to: {new_threshold}")
    
    def update_time_window(self, new_window_seconds: int) -> None:
        """Update the time window for analysis"""
        self.time_window_seconds = new_window_seconds
        self.logger.info(f"Time window updated to: {new_window_seconds} seconds")
    
    def add_suspicious_extension(self, extension: str) -> None:
        """Add a new suspicious extension to monitor"""
        ext_lower = extension.lower()
        if ext_lower not in self.suspicious_extensions:
            self.suspicious_extensions.append(ext_lower)
            self.logger.info(f"Added suspicious extension: {extension}")
    
    def get_detection_stats(self) -> Dict[str, any]:
        """Get current detection configuration stats"""
        return {
            "detection_threshold": self.detection_threshold,
            "time_window_seconds": self.time_window_seconds,
            "suspicious_extensions": self.suspicious_extensions,
            "suspicious_extension_count": len(self.suspicious_extensions)
        }