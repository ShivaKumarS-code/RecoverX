"""
File System Monitor for Ransomware Detection Tool
Uses watchdog library to monitor file system events in real-time
"""

import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from .logger import Logger


@dataclass
class FileEvent:
    """Represents a file system event"""
    timestamp: datetime
    file_path: str
    event_type: str  # 'modified', 'created', 'deleted', 'moved'
    file_size: int


class FileSystemMonitor:
    """Monitors file system for suspicious activities"""
    
    def __init__(self, logger: Logger, monitored_directory: str = "./test_files"):
        self.logger = logger
        self.monitored_directory = os.path.abspath(monitored_directory)
        self.observer = Observer()
        self.event_handler = FileEventHandler(self.logger)
        self.is_monitoring = False
        self.recent_events: List[FileEvent] = []
        
        # Ensure monitored directory exists
        os.makedirs(self.monitored_directory, exist_ok=True)
        
        self.logger.info(f"FileSystemMonitor initialized for directory: {self.monitored_directory}")
    
    def start_monitoring(self) -> bool:
        """Start monitoring the specified directory"""
        try:
            if self.is_monitoring:
                self.logger.warning("File system monitoring is already active")
                return True
            
            # Set up the event handler with reference to this monitor
            self.event_handler.set_monitor(self)
            
            # Schedule the observer
            self.observer.schedule(
                self.event_handler,
                self.monitored_directory,
                recursive=True
            )
            
            # Start the observer
            self.observer.start()
            self.is_monitoring = True
            
            self.logger.info(f"Started monitoring directory: {self.monitored_directory}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start file system monitoring: {str(e)}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop monitoring the file system"""
        try:
            if not self.is_monitoring:
                self.logger.warning("File system monitoring is not active")
                return True
            
            self.observer.stop()
            self.observer.join(timeout=5.0)  # Wait up to 5 seconds for clean shutdown
            self.is_monitoring = False
            
            self.logger.info("Stopped file system monitoring")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping file system monitoring: {str(e)}")
            return False
    
    def is_active(self) -> bool:
        """Check if monitoring is currently active"""
        return self.is_monitoring and self.observer.is_alive()
    
    def add_file_event(self, event_type: str, file_path: str) -> None:
        """Add a file event to the recent events list"""
        try:
            # Get file size if file exists
            file_size = 0
            if os.path.exists(file_path) and os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
            
            # Create file event
            file_event = FileEvent(
                timestamp=datetime.now(),
                file_path=file_path,
                event_type=event_type,
                file_size=file_size
            )
            
            # Add to recent events
            self.recent_events.append(file_event)
            
            # Keep only events from the last 60 seconds for analysis
            cutoff_time = datetime.now() - timedelta(seconds=60)
            self.recent_events = [
                event for event in self.recent_events 
                if event.timestamp > cutoff_time
            ]
            
            # Log the event
            self.logger.log_file_event(
                event_type, 
                file_path, 
                f"Size: {file_size} bytes"
            )
            
        except Exception as e:
            self.logger.error(f"Error processing file event: {str(e)}")
    
    def get_recent_events(self, seconds: int = 10) -> List[FileEvent]:
        """Get file events from the last N seconds"""
        cutoff_time = datetime.now() - timedelta(seconds=seconds)
        return [
            event for event in self.recent_events 
            if event.timestamp > cutoff_time
        ]
    
    def get_modification_count(self, seconds: int = 10) -> int:
        """Get count of file modifications in the last N seconds"""
        recent_events = self.get_recent_events(seconds)
        return len([event for event in recent_events if event.event_type == 'modified'])
    
    def get_monitored_directory(self) -> str:
        """Get the currently monitored directory"""
        return self.monitored_directory


class FileEventHandler(FileSystemEventHandler):
    """Handles file system events from watchdog"""
    
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger
        self.monitor: Optional[FileSystemMonitor] = None
    
    def set_monitor(self, monitor: FileSystemMonitor) -> None:
        """Set reference to the FileSystemMonitor"""
        self.monitor = monitor
    
    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events"""
        if not event.is_directory:
            self.logger.debug(f"File modified: {event.src_path}")
            if self.monitor:
                self.monitor.add_file_event('modified', event.src_path)
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events"""
        if not event.is_directory:
            self.logger.debug(f"File created: {event.src_path}")
            if self.monitor:
                self.monitor.add_file_event('created', event.src_path)
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file deletion events"""
        if not event.is_directory:
            self.logger.debug(f"File deleted: {event.src_path}")
            if self.monitor:
                self.monitor.add_file_event('deleted', event.src_path)
    
    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file move/rename events"""
        if not event.is_directory:
            self.logger.debug(f"File moved: {event.src_path} -> {event.dest_path}")
            if self.monitor:
                self.monitor.add_file_event('moved', event.dest_path)