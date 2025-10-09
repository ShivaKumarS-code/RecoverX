"""
Logging setup for Ransomware Detection Tool
Provides file and console logging with rotation
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional


class Logger:
    """Centralized logging configuration"""
    
    def __init__(self, log_directory: str = "./logs", log_level: str = "INFO"):
        self.log_directory = log_directory
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger = None
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Configure logging with file and console handlers"""
        # Create logs directory if it doesn't exist
        os.makedirs(self.log_directory, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("RansomwareDetectionTool")
        self.logger.setLevel(self.log_level)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handler with rotation
        log_file = os.path.join(self.log_directory, "ransomware_detection.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Log initialization
        self.logger.info("Logging system initialized")
        self.logger.info(f"Log directory: {self.log_directory}")
        self.logger.info(f"Log level: {logging.getLevelName(self.log_level)}")
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance"""
        return self.logger
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log critical message"""
        self.logger.critical(message)
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
    
    def log_file_event(self, event_type: str, file_path: str, details: str = "") -> None:
        """Log file system events"""
        message = f"FILE_EVENT: {event_type} - {file_path}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_threat_detection(self, threat_score: int, affected_files: list, reason: str) -> None:
        """Log threat detection events"""
        message = f"THREAT_DETECTED: Score={threat_score}, Files={len(affected_files)}, Reason={reason}"
        self.logger.warning(message)
        for file_path in affected_files:
            self.logger.warning(f"  Affected file: {file_path}")
    
    def log_backup_operation(self, operation: str, file_path: str, success: bool, details: str = "") -> None:
        """Log backup operations"""
        status = "SUCCESS" if success else "FAILED"
        message = f"BACKUP_{operation.upper()}: {status} - {file_path}"
        if details:
            message += f" - {details}"
        
        if success:
            self.logger.info(message)
        else:
            self.logger.error(message)
    
    def log_recovery_operation(self, file_path: str, success: bool, details: str = "") -> None:
        """Log recovery operations"""
        status = "SUCCESS" if success else "FAILED"
        message = f"RECOVERY: {status} - {file_path}"
        if details:
            message += f" - {details}"
        
        if success:
            self.logger.info(message)
        else:
            self.logger.error(message)