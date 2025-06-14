#!/usr/bin/env python3
"""
Vital Signs Data Processor - Startup Script
Handles initial setup and launches the web application
"""

import sys
import subprocess
import os
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]} (Compatible)")

def install_requirements():
    """Install required packages if not already installed"""
    print("📦 Checking and installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"
        ])
        print("✅ All packages installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)

def check_files():
    """Check if all required files exist"""
    required_files = [
        "app.py",
        "json_processor.py",
        "requirements.txt",
        "templates/base.html",
        "templates/index.html",
        "templates/about.html"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        sys.exit(1)
    
    print("✅ All required files found")

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "outputs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Working directories created")

def start_server():
    """Start the Flask application"""
    print("\n🚀 Starting Vital Signs Data Processor...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🔄 Starting server...")
    
    # Import and run the Flask app
    try:
        from app import app
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(1.5)
            webbrowser.open('http://localhost:5000')
        
        import threading
        threading.Thread(target=open_browser).start()
        
        # Run the Flask app
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    """Main function to run all setup steps"""
    print("=" * 60)
    print("🏥 VITAL SIGNS DATA PROCESSOR - WEB APPLICATION")
    print("=" * 60)
    
    # Run setup checks
    check_python_version()
    check_files()
    install_requirements()
    create_directories()
    
    print("\n✅ Setup complete! Starting web server...")
    print("📘 Instructions:")
    print("   1. Your browser will open automatically")
    print("   2. Drag & drop your JSON files or folders")
    print("   3. Click 'Process Files' to sort your data")
    print("   4. Download the organized ZIP file")
    print("\n💡 Tip: Keep this terminal window open while using the app")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main() 