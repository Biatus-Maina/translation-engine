#!/usr/bin/env python3
"""
Simple deployment checker for Translation Engine
Verifies the app is ready for Vercel deployment
"""

import os
import json

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking deployment files...")
    
    required_files = [
        "vercel.json",
        "requirements.txt", 
        "app/main.py",
        "app/__init__.py"
    ]
    
    all_good = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_good = False
    
    return all_good

def check_vercel_config():
    """Check vercel.json configuration"""
    print("\n🔧 Checking vercel.json...")
    
    try:
        with open("vercel.json", "r") as f:
            config = json.load(f)
        
        required_keys = ["version", "builds", "routes"]
        missing_keys = [key for key in required_keys if key not in config]
        
        if missing_keys:
            print(f"❌ Missing keys: {missing_keys}")
            return False
        
        print("✅ vercel.json configuration is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error reading vercel.json: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Translation Engine - Deployment Checker")
    print("=" * 50)
    
    # Check files
    if not check_files():
        print("\n❌ Some required files are missing!")
        return
    
    # Check Vercel config
    if not check_vercel_config():
        print("\n❌ Vercel configuration is invalid!")
        return
    
    print("\n🎉 All checks passed! Your app is ready for Vercel deployment.")
    print("\n📱 To deploy:")
    print("1. Push to GitHub: git add . && git commit -m 'Ready for Vercel' && git push")
    print("2. Go to vercel.com and import your repository")
    print("3. Click Deploy!")

if __name__ == "__main__":
    main() 