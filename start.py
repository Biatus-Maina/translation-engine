#!/usr/bin/env python3
"""
Translation Engine Startup Script
Run this script to start the FastAPI application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    return True

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting Translation Engine...")
    print("\n📱 Web Interface: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Alternative API Docs: http://localhost:8000/redoc")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

def main():
    """Main function"""
    print("🌍 Translation Engine - Professional Language Translation Service")
    print("=" * 60)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        print("Please make sure you're in the correct directory.")
        return
    
    # Check if app directory exists
    if not os.path.exists("app"):
        print("❌ app directory not found!")
        print("Please make sure you're in the correct directory.")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 