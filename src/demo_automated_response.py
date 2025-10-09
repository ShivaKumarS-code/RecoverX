#!/usr/bin/env python3
"""
Demonstration script for the Automated Response System

This script simulates ransomware-like activity to test the automated response
capabilities of the ransomware detection tool.
"""

import os
import time
import random
import shutil
from pathlib import Path


def create_test_files(test_dir: str, num_files: int = 10) -> list:
    """Create test files for demonstration"""
    test_path = Path(test_dir)
    test_path.mkdir(exist_ok=True)
    
    created_files = []
    
    for i in range(num_files):
        file_path = test_path / f"test_document_{i}.txt"
        
        # Create file with some content
        content = f"This is test document {i}\n" * random.randint(5, 20)
        content += f"Created at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += "This file contains important data that should be protected.\n"
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        created_files.append(str(file_path))
        print(f"Created test file: {file_path}")
    
    return created_files


def simulate_normal_activity(files: list, duration: int = 30):
    """Simulate normal file activity"""
    print(f"\nSimulating normal file activity for {duration} seconds...")
    
    start_time = time.time()
    while time.time() - start_time < duration:
        # Randomly modify a file
        file_path = random.choice(files)
        
        if os.path.exists(file_path):
            with open(file_path, 'a') as f:
                f.write(f"Normal update at {time.strftime('%H:%M:%S')}\n")
            
            print(f"Normal update: {os.path.basename(file_path)}")
        
        # Wait between modifications (normal pace)
        time.sleep(random.uniform(3, 8))


def simulate_ransomware_attack(files: list, attack_intensity: str = "moderate"):
    """Simulate ransomware-like activity"""
    print(f"\n🚨 SIMULATING RANSOMWARE ATTACK ({attack_intensity} intensity)")
    print("This should trigger the automated response system...")
    
    if attack_intensity == "light":
        # Modify files slowly (might not trigger detection)
        delay_range = (2, 4)
        files_to_modify = files[:3]
    elif attack_intensity == "moderate":
        # Modify files at moderate pace (should trigger detection)
        delay_range = (0.5, 1.5)
        files_to_modify = files[:6]
    else:  # heavy
        # Modify files rapidly (should definitely trigger detection and recovery)
        delay_range = (0.1, 0.5)
        files_to_modify = files
    
    for i, file_path in enumerate(files_to_modify):
        if os.path.exists(file_path):
            try:
                # Simulate encryption by modifying file content significantly
                with open(file_path, 'w') as f:
                    # Write encrypted-looking content
                    encrypted_content = "ENCRYPTED_DATA_" + "X" * random.randint(100, 500)
                    f.write(encrypted_content)
                
                print(f"⚠️  Simulated encryption: {os.path.basename(file_path)}")
                
                # Optionally rename file with suspicious extension
                if random.random() < 0.5:  # 50% chance
                    encrypted_path = file_path + ".encrypted"
                    shutil.move(file_path, encrypted_path)
                    print(f"⚠️  Renamed to: {os.path.basename(encrypted_path)}")
                
            except Exception as e:
                print(f"Error simulating attack on {file_path}: {e}")
        
        # Wait between file modifications
        if i < len(files_to_modify) - 1:
            time.sleep(random.uniform(*delay_range))
    
    print("🚨 Simulated ransomware attack completed")


def cleanup_test_files(test_dir: str):
    """Clean up test files"""
    test_path = Path(test_dir)
    
    if test_path.exists():
        try:
            shutil.rmtree(test_path)
            print(f"Cleaned up test directory: {test_dir}")
        except Exception as e:
            print(f"Error cleaning up {test_dir}: {e}")


def main():
    """Main demonstration function"""
    print("=" * 60)
    print("AUTOMATED RESPONSE SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    test_dir = "./test_files"
    
    try:
        # Create test files
        print("Setting up test environment...")
        test_files = create_test_files(test_dir, num_files=8)
        
        print(f"\nCreated {len(test_files)} test files in {test_dir}")
        print("Make sure the ransomware detection tool is running with:")
        print("  python main.py start")
        
        # Wait for user to start the monitoring system
        input("\nPress Enter when the monitoring system is running...")
        
        # Simulate normal activity first
        simulate_normal_activity(test_files, duration=20)
        
        print("\nWaiting 10 seconds before attack simulation...")
        time.sleep(10)
        
        # Ask user for attack intensity
        print("\nChoose attack intensity:")
        print("1. Light (might not trigger detection)")
        print("2. Moderate (should trigger detection)")
        print("3. Heavy (should trigger detection and recovery)")
        
        choice = input("Enter choice (1-3, default=2): ").strip()
        
        intensity_map = {"1": "light", "2": "moderate", "3": "heavy"}
        intensity = intensity_map.get(choice, "moderate")
        
        # Simulate ransomware attack
        simulate_ransomware_attack(test_files, intensity)
        
        print("\nAttack simulation completed.")
        print("Check the monitoring system logs to see the automated response.")
        print("The system should have:")
        print("- Detected the threat")
        print("- Created emergency backups")
        print("- Potentially triggered automated recovery (if threshold exceeded)")
        
        # Wait for user to observe results
        input("\nPress Enter to continue...")
        
        print("\nDemonstration completed!")
        print("Check the backup directory and logs for evidence of automated response.")
        
    except KeyboardInterrupt:
        print("\nDemonstration interrupted by user")
    except Exception as e:
        print(f"Error during demonstration: {e}")
    finally:
        # Ask if user wants to clean up
        cleanup = input("\nClean up test files? (y/N): ").strip().lower()
        if cleanup == 'y':
            cleanup_test_files(test_dir)


if __name__ == "__main__":
    main()