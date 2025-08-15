#!/usr/bin/env python3
"""
Virtual Environment Management Script for Translation Engine
Helps manage the virtual environment and project setup
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*20} {title} {'='*20}")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_venv_exists():
    """Check if virtual environment exists"""
    venv_path = Path("venv")
    if venv_path.exists() and (venv_path / "Scripts" / "python.exe").exists():
        print("✅ Virtual environment found")
        return True
    print("❌ Virtual environment not found")
    return False

def create_venv():
    """Create a new virtual environment"""
    print_header("Creating Virtual Environment")
    
    try:
        print("Creating virtual environment...")
        venv.create("venv", with_pip=True)
        print("✅ Virtual environment created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def activate_venv():
    """Activate the virtual environment"""
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate.bat"
        if os.path.exists(activate_script):
            print("✅ Virtual environment can be activated with:")
            print(f"   {activate_script}")
            return True
    else:  # Unix/Linux/Mac
        activate_script = "venv/bin/activate"
        if os.path.exists(activate_script):
            print("✅ Virtual environment can be activated with:")
            print(f"   source {activate_script}")
            return True
    
    print("❌ Virtual environment activation script not found")
    return False

def install_dependencies():
    """Install project dependencies"""
    print_header("Installing Dependencies")
    
    try:
        # Use the virtual environment's pip
        if os.name == 'nt':  # Windows
            pip_cmd = ["venv\\Scripts\\pip.exe", "install", "-r", "requirements.txt"]
        else:  # Unix/Linux/Mac
            pip_cmd = ["venv/bin/pip", "install", "-r", "requirements.txt"]
        
        print("Installing dependencies...")
        result = subprocess.run(pip_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    print_header("Testing Package Imports")
    
    try:
        # Use the virtual environment's python
        if os.name == 'nt':  # Windows
            python_cmd = ["venv\\Scripts\\python.exe", "-c", 
                         "import fastapi, uvicorn, deep_translator, langdetect; print('All packages imported successfully!')"]
        else:  # Unix/Linux/Mac
            python_cmd = ["venv/bin/python", "-c", 
                         "import fastapi, uvicorn, deep_translator, langdetect; print('All packages imported successfully!')"]
        
        result = subprocess.run(python_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All packages imported successfully!")
            return True
        else:
            print(f"❌ Package import test failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error testing imports: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions"""
    print_header("Usage Instructions")
    
    print("🌍 Translation Engine is ready to use!")
    print("\n📱 To start the web interface:")
    if os.name == 'nt':  # Windows
        print("   • Double-click 'start.bat' (easiest)")
        print("   • Or run: python start.py")
        print("   • Or activate venv and run: python -m uvicorn app.main:app --reload")
    else:  # Unix/Linux/Mac
        print("   • Run: python start.py")
        print("   • Or activate venv and run: python -m uvicorn app.main:app --reload")
    
    print("\n🧪 To test the application:")
    print("   • Run: python test_app.py")
    print("   • Run: python demo.py")
    
    print("\n🌐 Once running, visit:")
    print("   • Web Interface: http://localhost:8000")
    print("   • API Docs: http://localhost:8000/docs")
    
    print("\n🔧 Virtual Environment Management:")
    if os.name == 'nt':  # Windows
        print("   • Activate: venv\\Scripts\\activate.bat")
        print("   • Deactivate: deactivate")
    else:  # Unix/Linux/Mac
        print("   • Activate: source venv/bin/activate")
        print("   • Deactivate: deactivate")

def main():
    """Main function"""
    print("🌍 Translation Engine - Virtual Environment Manager")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check if virtual environment exists
    if not check_venv_exists():
        print("\nCreating new virtual environment...")
        if not create_venv():
            return
    
    # Check activation
    if not activate_venv():
        return
    
    # Check if dependencies are installed
    if not os.path.exists("venv/Scripts/pip.exe") and not os.path.exists("venv/bin/pip"):
        print("❌ pip not found in virtual environment")
        return
    
    # Install dependencies if needed
    if not test_imports():
        print("\nInstalling dependencies...")
        if not install_dependencies():
            return
        
        # Test imports again
        if not test_imports():
            print("❌ Dependencies installation failed")
            return
    
    # Show usage instructions
    show_usage_instructions()

if __name__ == "__main__":
    main() 