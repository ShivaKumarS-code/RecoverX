#!/usr/bin/env python3
"""
Dashboard Startup Script

Quick launcher for the web dashboard with automatic browser opening.
"""

import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_socketio
        return True
    except ImportError:
        return False


def install_dependencies():
    """Install required dependencies"""
    print("Installing web dashboard dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    """Main startup function"""
    print("=" * 60)
    print("🛡️  RANSOMWARE DETECTION TOOL - WEB DASHBOARD")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('web_app.py').exists():
        print("❌ Error: web_app.py not found")
        print("   Please run this script from the project root directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("📦 Installing required dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            print("   Please run: pip install -r requirements.txt")
            return
        print("✅ Dependencies installed successfully")
    
    print("🚀 Starting web dashboard...")
    print("📊 Dashboard URL: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Wait a moment then open browser
    def open_browser():
        time.sleep(2)
        try:
            webbrowser.open('http://localhost:5000')
            print("🌐 Opening dashboard in your default browser...")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("   Please manually open: http://localhost:5000")
    
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start the web application
    try:
        # Use subprocess instead of os.system for better error handling
        subprocess.run([sys.executable, 'web_app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting dashboard: {e}")
        print("   Try running directly: python web_app.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("   Try running directly: python web_app.py")


if __name__ == "__main__":
    main()