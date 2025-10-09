"""
Configuration Manager for Ransomware Detection Tool
Handles loading and validation of JSON configuration files
"""

import json
import os
from typing import Dict, Any, List


class ConfigManager:
    """Manages configuration loading and validation"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = {}
        self.default_config = {
            "monitored_directory": "./test_files",
            "backup_directory": "./backups",
            "log_directory": "./logs",
            "alert_email": "",
            "detection_threshold": 5,
            "backup_retention": 5,
            "time_window_seconds": 10,
            "response_threshold": 50,
            "suspicious_extensions": [".encrypted", ".locked", ".crypto", ".crypt"]
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                    print(f"Configuration loaded from {self.config_path}")
            else:
                print(f"Configuration file {self.config_path} not found, using defaults")
                self.config = self.default_config.copy()
                self.save_config()
            
            # Validate and fill missing keys with defaults
            self._validate_config()
            return self.config
            
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            print("Using default configuration")
            self.config = self.default_config.copy()
            return self.config
        except Exception as e:
            print(f"Error loading configuration: {e}")
            print("Using default configuration")
            self.config = self.default_config.copy()
            return self.config
    
    def save_config(self) -> bool:
        """Save current configuration to JSON file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def _validate_config(self) -> None:
        """Validate configuration and fill missing values with defaults"""
        for key, default_value in self.default_config.items():
            if key not in self.config:
                self.config[key] = default_value
                print(f"Added missing configuration key '{key}' with default value")
        
        # Validate specific types
        if not isinstance(self.config.get("detection_threshold"), int):
            self.config["detection_threshold"] = self.default_config["detection_threshold"]
        
        if not isinstance(self.config.get("backup_retention"), int):
            self.config["backup_retention"] = self.default_config["backup_retention"]
        
        if not isinstance(self.config.get("time_window_seconds"), int):
            self.config["time_window_seconds"] = self.default_config["time_window_seconds"]
        
        if not isinstance(self.config.get("response_threshold"), int):
            self.config["response_threshold"] = self.default_config["response_threshold"]
        
        if not isinstance(self.config.get("suspicious_extensions"), list):
            self.config["suspicious_extensions"] = self.default_config["suspicious_extensions"]
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value by key"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
    
    def get_monitored_directory(self) -> str:
        """Get the directory to monitor"""
        return self.config.get("monitored_directory", "./test_files")
    
    def get_backup_directory(self) -> str:
        """Get the backup directory"""
        return self.config.get("backup_directory", "./backups")
    
    def get_log_directory(self) -> str:
        """Get the log directory"""
        return self.config.get("log_directory", "./logs")
    
    def get_detection_threshold(self) -> int:
        """Get the detection threshold"""
        return self.config.get("detection_threshold", 5)
    
    def get_suspicious_extensions(self) -> List[str]:
        """Get list of suspicious file extensions"""
        return self.config.get("suspicious_extensions", [".encrypted", ".locked", ".crypto", ".crypt"])