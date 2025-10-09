#!/usr/bin/env python3
"""
Quick Demo Launcher for Ransomware Detection & Recovery Tool

This script provides an easy way to run different demonstration scenarios.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_requirements():
    """Check if all requirements are met"""
    print("Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print("✅ Python version OK")
    
    # Check if main files exist
    required_files = ['main.py', 'config.json', 'requirements.txt']
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Required file missing: {file}")
            return False
    print("✅ Required files present")
    
    # Check if dependencies are installed
    try:
        import watchdog
        print("✅ Dependencies installed")
    except ImportError:
        print("❌ Dependencies not installed. Run: pip install -r requirements.txt")
        return False
    
    return True


def run_full_demo():
    """Run the complete demonstration"""
    print("\n🎯 Starting Complete Demonstration")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, 'demo.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed with error: {e}")
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")


def run_ransomware_simulation(attack_type, intensity):
    """Run ransomware simulation"""
    print(f"\n🦠 Starting Ransomware Simulation: {attack_type} ({intensity})")
    print("=" * 50)
    
    try:
        cmd = [sys.executable, 'src/ransomware_simulator.py', attack_type, '--intensity', intensity]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Simulation failed with error: {e}")
    except KeyboardInterrupt:
        print("\n⏹️  Simulation interrupted by user")


def run_monitoring_system():
    """Start the monitoring system"""
    print("\n👁️  Starting Monitoring System")
    print("=" * 50)
    print("Press Ctrl+C to stop monitoring")
    
    try:
        subprocess.run([sys.executable, 'main.py', 'start'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Monitoring failed with error: {e}")
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring stopped by user")


def show_system_status():
    """Show current system status"""
    print("\n📊 System Status")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, 'main.py', 'status'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Status check failed with error: {e}")


def interactive_menu():
    """Show interactive menu for demo options"""
    while True:
        print("\n" + "=" * 60)
        print("🛡️  RANSOMWARE DETECTION TOOL - DEMO LAUNCHER")
        print("=" * 60)
        
        print("\nChoose a demonstration option:")
        print("1. 🎯 Complete System Demonstration (Recommended)")
        print("2. 🦠 Ransomware Simulation Only")
        print("3. 👁️  Start Monitoring System")
        print("4. 📊 Check System Status")
        print("5. ❓ Help & Information")
        print("6. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            run_full_demo()
        elif choice == '2':
            simulation_menu()
        elif choice == '3':
            run_monitoring_system()
        elif choice == '4':
            show_system_status()
        elif choice == '5':
            show_help()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-6.")


def simulation_menu():
    """Show ransomware simulation options"""
    print("\n🦠 Ransomware Simulation Options")
    print("=" * 40)
    
    print("\nAttack Types:")
    print("1. CryptoLocker (encrypts and renames files)")
    print("2. File Renamer (renames with random extensions)")
    print("3. Rapid Encryptor (fast attack - triggers detection)")
    print("4. Stealth Encryptor (slow attack - may avoid detection)")
    
    attack_choice = input("\nChoose attack type (1-4): ").strip()
    attack_map = {
        '1': 'crypto_locker',
        '2': 'file_renamer', 
        '3': 'rapid_encryptor',
        '4': 'stealth_encryptor'
    }
    
    if attack_choice not in attack_map:
        print("❌ Invalid choice")
        return
    
    print("\nIntensity Levels:")
    print("1. Light (slow, few files)")
    print("2. Moderate (normal speed)")
    print("3. Heavy (fast, many files)")
    
    intensity_choice = input("\nChoose intensity (1-3): ").strip()
    intensity_map = {
        '1': 'light',
        '2': 'moderate',
        '3': 'heavy'
    }
    
    if intensity_choice not in intensity_map:
        print("❌ Invalid choice")
        return
    
    attack_type = attack_map[attack_choice]
    intensity = intensity_map[intensity_choice]
    
    run_ransomware_simulation(attack_type, intensity)


def show_help():
    """Show help information"""
    print("\n❓ Help & Information")
    print("=" * 40)
    
    print("\n📖 About This Tool:")
    print("This ransomware detection tool demonstrates cybersecurity concepts")
    print("through real-time file monitoring, threat detection, and automated recovery.")
    
    print("\n🎯 Complete Demonstration:")
    print("- Sets up test files and monitoring system")
    print("- Shows normal file activity (no alerts)")
    print("- Simulates ransomware attack")
    print("- Demonstrates automated detection and recovery")
    print("- Provides comprehensive statistics")
    
    print("\n🦠 Ransomware Simulation:")
    print("- Tests different attack patterns")
    print("- Configurable intensity levels")
    print("- Safe simulation environment")
    print("- No actual harm to real files")
    
    print("\n👁️  Monitoring System:")
    print("- Real-time file system monitoring")
    print("- Threat detection and alerting")
    print("- Automated backup and recovery")
    print("- Comprehensive logging")
    
    print("\n📚 Educational Value:")
    print("- File system programming")
    print("- Security pattern recognition")
    print("- Automated response systems")
    print("- Incident response procedures")
    
    print("\n⚠️  Important Notes:")
    print("- This is for educational purposes only")
    print("- Safe to run - no actual malware")
    print("- Creates test files in ./test_files directory")
    print("- Backups stored in ./backups directory")
    
    input("\nPress Enter to continue...")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Demo Launcher for Ransomware Detection & Recovery Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_demo.py                    # Interactive menu
  python run_demo.py --full             # Run complete demonstration
  python run_demo.py --simulate crypto_locker --intensity moderate
  python run_demo.py --monitor          # Start monitoring system
  python run_demo.py --status           # Check system status
        """
    )
    
    parser.add_argument('--full', action='store_true', help='Run complete demonstration')
    parser.add_argument('--simulate', choices=['crypto_locker', 'file_renamer', 'rapid_encryptor', 'stealth_encryptor'], help='Run ransomware simulation')
    parser.add_argument('--intensity', choices=['light', 'moderate', 'heavy'], default='moderate', help='Simulation intensity')
    parser.add_argument('--monitor', action='store_true', help='Start monitoring system')
    parser.add_argument('--status', action='store_true', help='Show system status')
    
    args = parser.parse_args()
    
    # Check requirements first
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        return
    
    # Handle command line arguments
    if args.full:
        run_full_demo()
    elif args.simulate:
        run_ransomware_simulation(args.simulate, args.intensity)
    elif args.monitor:
        run_monitoring_system()
    elif args.status:
        show_system_status()
    else:
        # Show interactive menu
        interactive_menu()


if __name__ == "__main__":
    main()