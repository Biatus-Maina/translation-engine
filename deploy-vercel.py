#!/usr/bin/env python3
"""
Vercel Deployment Helper Script
Helps prepare and test the Translation Engine for Vercel deployment
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*20} {title} {'='*20}")

def check_vercel_config():
    """Check if Vercel configuration files exist"""
    print_header("Checking Vercel Configuration")
    
    required_files = [
        "vercel.json",
        "requirements.txt",
        "app/main.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files found")
    return True

def validate_vercel_json():
    """Validate vercel.json configuration"""
    print_header("Validating vercel.json")
    
    try:
        with open("vercel.json", "r") as f:
            config = json.load(f)
        
        required_keys = ["version", "builds", "routes"]
        missing_keys = [key for key in required_keys if key not in config]
        
        if missing_keys:
            print(f"❌ Missing required keys in vercel.json: {missing_keys}")
            return False
        
        print("✅ vercel.json is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in vercel.json: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading vercel.json: {e}")
        return False

def check_requirements():
    """Check requirements.txt for Vercel compatibility"""
    print_header("Checking Requirements")
    
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()
        
        # Check for specific versions (recommended for Vercel)
        if "==" in requirements:
            print("✅ Requirements have specific versions (good for Vercel)")
        else:
            print("⚠️  Requirements use version ranges (consider specific versions)")
        
        # Check for problematic packages
        problematic = ["uvicorn[standard]", "uvicorn[extras]"]
        found_problematic = [pkg for pkg in problematic if pkg in requirements]
        
        if found_problematic:
            print(f"⚠️  Found potentially problematic packages: {found_problematic}")
            print("   Consider using 'uvicorn' instead of 'uvicorn[standard]'")
        
        print("✅ Requirements.txt looks good")
        return True
        
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def test_local_app():
    """Test if the app runs locally"""
    print_header("Testing Local Application")
    
    try:
        # Test imports
        print("Testing imports...")
        result = subprocess.run([
            sys.executable, "-c", 
            "from app.main import app; print('✅ App imports successfully')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ App imports successfully")
        else:
            print(f"❌ Import failed: {result.stderr}")
            return False
        
        # Test health endpoint
        print("Testing health endpoint...")
        result = subprocess.run([
            sys.executable, "-c", 
            "from app.main import app; print('✅ Health endpoint available')"
        ], capture_output=True, text=True)
        
        print("✅ Local app test passed")
        return True
        
    except Exception as e:
        print(f"❌ Local app test failed: {e}")
        return False

def create_vercel_ignore():
    """Create .vercelignore file"""
    print_header("Creating .vercelignore")
    
    ignore_content = """# Virtual environment
venv/
env/
.venv/

# Development files
*.pyc
__pycache__/
.pytest_cache/
.coverage

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Test files
test_*.py
demo.py

# Documentation
VENV_SETUP.md
QUICK_START.md
README.md

# Startup scripts
start.py
start.bat
activate_venv.bat
manage_venv.py

# Git
.git/
.gitignore
"""
    
    try:
        with open(".vercelignore", "w") as f:
            f.write(ignore_content)
        print("✅ .vercelignore created")
        return True
    except Exception as e:
        print(f"❌ Failed to create .vercelignore: {e}")
        return False

def show_deployment_steps():
    """Show deployment steps"""
    print_header("Deployment Steps")
    
    print("🚀 To deploy on Vercel:")
    print("\n1. Push to GitHub:")
    print("   git add .")
    print("   git commit -m 'Prepare for Vercel deployment'")
    print("   git push origin main")
    
    print("\n2. Deploy on Vercel:")
    print("   - Go to vercel.com")
    print("   - Click 'New Project'")
    print("   - Import your GitHub repository")
    print("   - Click 'Deploy'")
    
    print("\n3. Alternative: Use Vercel CLI")
    print("   npm i -g vercel")
    print("   vercel login")
    print("   vercel")
    
    print("\n📱 Your app will be available at:")
    print("   https://your-app.vercel.app")
    print("   https://your-app.vercel.app/api/health")
    print("   https://your-app.vercel.app/docs")

def main():
    """Main function"""
    print("🚀 Translation Engine - Vercel Deployment Helper")
    print("=" * 60)
    
    # Check configuration
    if not check_vercel_config():
        print("\n❌ Configuration check failed. Please fix the issues above.")
        return
    
    if not validate_vercel_json():
        print("\n❌ Vercel configuration validation failed.")
        return
    
    if not check_requirements():
        print("\n❌ Requirements check failed.")
        return
    
    if not test_local_app():
        print("\n❌ Local app test failed.")
        return
    
    # Create .vercelignore
    create_vercel_ignore()
    
    print_header("✅ All Checks Passed!")
    print("Your Translation Engine is ready for Vercel deployment!")
    
    # Show deployment steps
    show_deployment_steps()
    
    print("\n📚 For detailed instructions, see VERCEL_DEPLOYMENT.md")

if __name__ == "__main__":
    main() 