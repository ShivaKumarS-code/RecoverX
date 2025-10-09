#!/usr/bin/env python3
"""
Ransomware Simulation Script

This script simulates various types of ransomware behavior for testing
the detection and recovery capabilities of the ransomware detection tool.
"""

import os
import time
import random
import shutil
import argparse
from pathlib import Path
from typing import List, Dict


class RansomwareSimulator:
    """Simulates different types of ransomware attacks for testing"""
    
    def __init__(self, target_directory: str):
        self.target_directory = Path(target_directory)
        self.target_directory.mkdir(exist_ok=True)
        self.created_files = []
        self.attack_patterns = {
            'crypto_locker': self._simulate_crypto_locker,
            'file_renamer': self._simulate_file_renamer,
            'rapid_encryptor': self._simulate_rapid_encryptor,
            'stealth_encryptor': self._simulate_stealth_encryptor
        }
    
    def create_test_files(self, num_files: int = 10, file_types: List[str] = None) -> List[str]:
        """Create test files with various content types"""
        if file_types is None:
            file_types = ['.txt', '.doc', '.pdf', '.jpg', '.xlsx']
        
        print(f"Creating {num_files} test files...")
        
        for i in range(num_files):
            # Choose random file type
            file_ext = random.choice(file_types)
            file_path = self.target_directory / f"test_file_{i:03d}{file_ext}"
            
            # Create file with realistic content
            content = self._generate_file_content(file_ext, i)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.created_files.append(str(file_path))
            print(f"  Created: {file_path.name}")
        
        return self.created_files
    
    def _generate_file_content(self, file_ext: str, file_num: int) -> str:
        """Generate realistic file content based on extension"""
        base_content = f"Test File {file_num}\n"
        base_content += f"Created: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        base_content += f"File Type: {file_ext}\n\n"
        
        if file_ext == '.txt':
            content = base_content + "This is a text document with important information.\n" * 10
        elif file_ext == '.doc':
            content = base_content + "DOCUMENT CONTENT: " + "Important business document. " * 20
        elif file_ext == '.pdf':
            content = base_content + "PDF CONTENT: " + "Research paper content. " * 15
        elif file_ext == '.jpg':
            content = base_content + "IMAGE METADATA: " + "Photo taken on vacation. " * 5
        elif file_ext == '.xlsx':
            content = base_content + "SPREADSHEET DATA: " + "Financial data, Quarter 1. " * 12
        else:
            content = base_content + "Generic file content. " * 8
        
        return content
    
    def simulate_attack(self, attack_type: str, intensity: str = 'moderate') -> Dict:
        """Simulate a specific type of ransomware attack"""
        if attack_type not in self.attack_patterns:
            raise ValueError(f"Unknown attack type: {attack_type}")
        
        print(f"\n🚨 SIMULATING {attack_type.upper()} ATTACK ({intensity} intensity)")
        print("=" * 50)
        
        start_time = time.time()
        result = self.attack_patterns[attack_type](intensity)
        end_time = time.time()
        
        result['attack_duration'] = end_time - start_time
        result['attack_type'] = attack_type
        result['intensity'] = intensity
        
        print(f"Attack simulation completed in {result['attack_duration']:.2f} seconds")
        return result
    
    def _simulate_crypto_locker(self, intensity: str) -> Dict:
        """Simulate CryptoLocker-style ransomware"""
        print("Simulating CryptoLocker behavior:")
        print("- Encrypts files with .encrypted extension")
        print("- Modifies file content to appear encrypted")
        print("- Creates ransom note")
        
        # Set timing based on intensity
        timing = self._get_attack_timing(intensity)
        files_affected = 0
        
        for file_path in self.created_files:
            if os.path.exists(file_path):
                try:
                    # Read original content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    # "Encrypt" content
                    encrypted_content = self._encrypt_content(original_content)
                    
                    # Write encrypted content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(encrypted_content)
                    
                    # Rename with .encrypted extension
                    encrypted_path = file_path + '.encrypted'
                    shutil.move(file_path, encrypted_path)
                    
                    print(f"  ⚠️  Encrypted: {Path(file_path).name} -> {Path(encrypted_path).name}")
                    files_affected += 1
                    
                    time.sleep(timing['file_delay'])
                    
                except Exception as e:
                    print(f"  Error encrypting {file_path}: {e}")
        
        # Create ransom note
        self._create_ransom_note("CryptoLocker")
        
        return {
            'files_affected': files_affected,
            'ransom_note_created': True,
            'extensions_changed': True
        }
    
    def _simulate_file_renamer(self, intensity: str) -> Dict:
        """Simulate ransomware that renames files with random extensions"""
        print("Simulating File Renamer behavior:")
        print("- Renames files with random extensions")
        print("- Keeps original content but makes files inaccessible")
        
        timing = self._get_attack_timing(intensity)
        files_affected = 0
        random_extensions = ['.locked', '.crypto', '.vault', '.secure', '.xxx']
        
        for file_path in self.created_files:
            if os.path.exists(file_path):
                try:
                    # Choose random extension
                    new_ext = random.choice(random_extensions)
                    new_path = file_path + new_ext
                    
                    # Rename file
                    shutil.move(file_path, new_path)
                    
                    print(f"  ⚠️  Renamed: {Path(file_path).name} -> {Path(new_path).name}")
                    files_affected += 1
                    
                    time.sleep(timing['file_delay'])
                    
                except Exception as e:
                    print(f"  Error renaming {file_path}: {e}")
        
        self._create_ransom_note("FileRenamer")
        
        return {
            'files_affected': files_affected,
            'ransom_note_created': True,
            'extensions_changed': True
        }
    
    def _simulate_rapid_encryptor(self, intensity: str) -> Dict:
        """Simulate very fast ransomware that should definitely trigger detection"""
        print("Simulating Rapid Encryptor behavior:")
        print("- Encrypts files very quickly")
        print("- Should trigger detection systems immediately")
        
        files_affected = 0
        
        # Process all files as quickly as possible
        for file_path in self.created_files:
            if os.path.exists(file_path):
                try:
                    # Quickly overwrite with encrypted content
                    encrypted_content = "RAPID_ENCRYPTION_" + "X" * 200
                    
                    with open(file_path, 'w') as f:
                        f.write(encrypted_content)
                    
                    print(f"  ⚠️  Rapidly encrypted: {Path(file_path).name}")
                    files_affected += 1
                    
                    # Very short delay to simulate rapid encryption
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"  Error encrypting {file_path}: {e}")
        
        self._create_ransom_note("RapidEncryptor")
        
        return {
            'files_affected': files_affected,
            'ransom_note_created': True,
            'extensions_changed': False
        }
    
    def _simulate_stealth_encryptor(self, intensity: str) -> Dict:
        """Simulate slow, stealthy ransomware that might avoid detection"""
        print("Simulating Stealth Encryptor behavior:")
        print("- Encrypts files slowly to avoid detection")
        print("- May not trigger threshold-based detection")
        
        files_affected = 0
        
        # Process files with long delays
        for i, file_path in enumerate(self.created_files[:3]):  # Only affect first 3 files
            if os.path.exists(file_path):
                try:
                    # Read and encrypt content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    encrypted_content = self._encrypt_content(original_content)
                    
                    with open(file_path, 'w') as f:
                        f.write(encrypted_content)
                    
                    print(f"  ⚠️  Stealthily encrypted: {Path(file_path).name}")
                    files_affected += 1
                    
                    # Long delay between files
                    if i < 2:  # Don't wait after last file
                        print(f"    Waiting 15 seconds before next file...")
                        time.sleep(15)
                    
                except Exception as e:
                    print(f"  Error encrypting {file_path}: {e}")
        
        self._create_ransom_note("StealthEncryptor")
        
        return {
            'files_affected': files_affected,
            'ransom_note_created': True,
            'extensions_changed': False
        }
    
    def _get_attack_timing(self, intensity: str) -> Dict:
        """Get timing parameters based on attack intensity"""
        timing_configs = {
            'light': {'file_delay': 3.0, 'batch_delay': 10.0},
            'moderate': {'file_delay': 1.0, 'batch_delay': 5.0},
            'heavy': {'file_delay': 0.2, 'batch_delay': 1.0}
        }
        return timing_configs.get(intensity, timing_configs['moderate'])
    
    def _encrypt_content(self, content: str) -> str:
        """Simulate file encryption by scrambling content"""
        # Simple "encryption" simulation
        encrypted = "ENCRYPTED_FILE_HEADER\n"
        encrypted += "Original size: " + str(len(content)) + " bytes\n"
        encrypted += "Encryption algorithm: AES-256 (simulated)\n"
        encrypted += "Key ID: " + str(random.randint(1000, 9999)) + "\n"
        encrypted += "=" * 50 + "\n"
        encrypted += "ENCRYPTED_DATA: " + "X" * min(len(content), 500)
        return encrypted
    
    def _create_ransom_note(self, attack_type: str):
        """Create a ransom note file"""
        ransom_note_path = self.target_directory / "RANSOM_NOTE.txt"
        
        ransom_content = f"""
YOUR FILES HAVE BEEN ENCRYPTED BY {attack_type.upper()}!

All your important files have been encrypted with strong encryption.
Your documents, photos, databases and other important files are no longer accessible.

To recover your files, you need to pay a ransom of $500 in Bitcoin.

This is a SIMULATION for testing purposes only.
No actual encryption has occurred.

Attack Type: {attack_type}
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}

DO NOT PANIC - This is just a test!
"""
        
        with open(ransom_note_path, 'w') as f:
            f.write(ransom_content)
        
        print(f"  📝 Created ransom note: {ransom_note_path.name}")
    
    def cleanup(self):
        """Clean up all created files and directories"""
        print(f"\nCleaning up test files in {self.target_directory}...")
        
        try:
            if self.target_directory.exists():
                shutil.rmtree(self.target_directory)
                print(f"✓ Cleaned up: {self.target_directory}")
        except Exception as e:
            print(f"✗ Error cleaning up: {e}")


def main():
    """Main function for ransomware simulation"""
    parser = argparse.ArgumentParser(
        description="Ransomware Simulation Tool for Testing Detection Systems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Attack Types:
  crypto_locker    - Encrypts files and adds .encrypted extension
  file_renamer     - Renames files with random extensions
  rapid_encryptor  - Very fast encryption (should trigger detection)
  stealth_encryptor - Slow encryption (might avoid detection)

Intensity Levels:
  light     - Slow attack, few files affected
  moderate  - Normal speed attack
  heavy     - Fast attack, many files affected

Examples:
  python ransomware_simulator.py crypto_locker --intensity moderate
  python ransomware_simulator.py rapid_encryptor --target ./test_files
  python ransomware_simulator.py stealth_encryptor --files 5
        """
    )
    
    parser.add_argument(
        'attack_type',
        choices=['crypto_locker', 'file_renamer', 'rapid_encryptor', 'stealth_encryptor'],
        help='Type of ransomware attack to simulate'
    )
    
    parser.add_argument(
        '--target',
        default='./test_files',
        help='Target directory for simulation (default: ./test_files)'
    )
    
    parser.add_argument(
        '--intensity',
        choices=['light', 'moderate', 'heavy'],
        default='moderate',
        help='Attack intensity (default: moderate)'
    )
    
    parser.add_argument(
        '--files',
        type=int,
        default=8,
        help='Number of test files to create (default: 8)'
    )
    
    parser.add_argument(
        '--no-cleanup',
        action='store_true',
        help='Do not clean up files after simulation'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("RANSOMWARE SIMULATION TOOL")
    print("=" * 60)
    print(f"Attack Type: {args.attack_type}")
    print(f"Intensity: {args.intensity}")
    print(f"Target Directory: {args.target}")
    print(f"Test Files: {args.files}")
    
    # Initialize simulator
    simulator = RansomwareSimulator(args.target)
    
    try:
        # Create test files
        print(f"\n1. Setting up test environment...")
        test_files = simulator.create_test_files(args.files)
        
        print(f"\n2. Test files created successfully!")
        print("   Make sure the ransomware detection tool is running:")
        print("   python main.py start")
        
        # Wait for user confirmation
        input("\nPress Enter when the detection system is ready...")
        
        # Run simulation
        print(f"\n3. Starting {args.attack_type} simulation...")
        result = simulator.simulate_attack(args.attack_type, args.intensity)
        
        # Display results
        print(f"\n4. Simulation Results:")
        print(f"   Attack Type: {result['attack_type']}")
        print(f"   Intensity: {result['intensity']}")
        print(f"   Files Affected: {result['files_affected']}")
        print(f"   Duration: {result['attack_duration']:.2f} seconds")
        print(f"   Ransom Note: {'Created' if result['ransom_note_created'] else 'Not Created'}")
        print(f"   Extensions Changed: {'Yes' if result['extensions_changed'] else 'No'}")
        
        print(f"\n5. Check the detection system for:")
        print("   - Threat detection alerts")
        print("   - Automatic backup creation")
        print("   - Recovery actions (if threshold exceeded)")
        print("   - Log entries showing system response")
        
        input("\nPress Enter to continue...")
        
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Cleanup
        if not args.no_cleanup:
            cleanup = input("\nClean up test files? (Y/n): ").strip().lower()
            if cleanup != 'n':
                simulator.cleanup()
        else:
            print("Skipping cleanup as requested")
    
    print("\nSimulation completed!")


if __name__ == "__main__":
    main()